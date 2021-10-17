import hashlib
import json
import random
import string
import time
import logging

from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)

API_DOMAIN = {
    "CN": "open-cn.aqara.com",
    "USA": "open-usa.aqara.com",
    "KR": "open-kr.aqara.com",
    "RU": "open-ru.aqara.com",
    "GER": "open-ger.aqara.com",
}

APP_ID = "88110776288481280040ace0"
KEY_ID = "K.881107763014836224"
APP_KEY = "t7g6qhx4nmbeqmfq1w6yksucnbrofsgs"


def get_random_string(length: int):
    seq = string.ascii_uppercase + string.digits
    return "".join((random.choice(seq) for _ in range(length)))


# 生成Headers中的sign
def gen_sign(
    access_token: str,
    app_id: str,
    key_id: str,
    nonce: str,
    timestamp: str,
    app_key: str,
):
    """Signature in headers, see https://opendoc.aqara.cn/docs/%E4%BA%91%E5%AF%B9%E6%8E%A5%E5%BC%80%E5%8F%91%E6%89%8B%E5%86%8C/API%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97/Sign%E7%94%9F%E6%88%90%E8%A7%84%E5%88%99.html"""
    s = f"Appid={app_id}&Keyid={key_id}&Nonce={nonce}&Time={timestamp}{app_key}"
    if access_token and len(access_token) > 0:
        s = f"AccessToken={access_token}&{s}"
    s = s.lower()
    sign = hashlib.md5(s.encode("utf-8")).hexdigest()
    return sign


class AiotCloud:
    access_token = None
    refresh_token = None
    update_token_event_callback = None

    def __init__(self, session: ClientSession):
        self.app_id = APP_ID
        self.key_id = KEY_ID
        self.app_key = APP_KEY
        self.session = session
        self.options = None
        self.set_country("CN")

    def set_options(self, options):
        """ set hass options """
        self.options = options

    def get_options(self):
        """ get hass options """
        return self.options

    def set_country(self, country: str):
        """ set aiot country """
        self.country = country
        self.api_url = f"https://{API_DOMAIN[country]}/v3.0/open/api"

    def _get_request_headers(self):
        """生成Headers"""
        nonce = get_random_string(16)
        timestamp = str(int(round(time.time() * 1000)))
        sign = gen_sign(
            self.access_token, self.app_id, self.key_id, nonce, timestamp, self.app_key
        )
        headers = {
            "Content-Type": "application/json",
            "Appid": self.app_id,
            "Keyid": self.key_id,
            "Nonce": nonce,
            "Time": timestamp,
            "Sign": sign,
            "Lang": "zh",
        }
        if self.access_token:
            headers["Accesstoken"] = self.access_token
        return headers

    async def _async_invoke_aqara_cloud_api(
        self, intent: str, only_result: bool = True, list_data: bool = False, **kwargs
    ):
        """调用Aqara Api"""
        try:
            empty_keys = []
            for k, v in kwargs.items():
                if v is None:
                    empty_keys.append(k)
            [kwargs.pop(x) for x in empty_keys]
            payload = (
                {"intent": intent, "data": [kwargs]}
                if list_data
                else {"intent": intent, "data": kwargs}
            )
            r = await self.session.post(
                url=self.api_url,
                data=json.dumps(payload),
                headers=self._get_request_headers(),
            )
            raw = await r.read()
            jo = json.loads(raw)

            if only_result:
                # 这里的异常处理需要优化
                if jo["code"] != 0:
                    # 调用Aiot api失败，返回值
                    _LOGGER.warn(f"Call Aiot api failed，return：{jo}")
                    if jo["code"] == 108:
                        # 令牌过期或异常，正在尝试自动刷新
                        _LOGGER.warn(f"Aiot token expired, trying to auto refresh！")
                        new_jo = await self.async_refresh_token(self.refresh_token)
                        if new_jo["code"] == 0:
                            # Aiot令牌更新成功！
                            _LOGGER.info(f"Aiot token refresh successfully！")
                            return await self._async_invoke_aqara_cloud_api(
                                intent, only_result, list_data, **kwargs
                            )
                        else:
                            # Aiot令牌更新失败，请重新授权
                            _LOGGER.warn("Aiot token refresh failed, please do authorization again！")
                return jo.get("result")
            else:
                return jo

        except Exception as ex:
            _LOGGER.error(ex)

    async def async_get_auth_code(
        self, account: str, account_type: int, access_token_validity: str = "7d"
    ):
        """获取授权验证码"""
        return await self._async_invoke_aqara_cloud_api(
            intent="config.auth.getAuthCode",
            only_result=False,
            account=account,
            accountType=account_type,
            accessTokenValidity=access_token_validity,
        )

    async def async_get_token(self, authCode: str, account: str, account_type: int):
        """获取访问令牌"""
        jo = await self._async_invoke_aqara_cloud_api(
            intent="config.auth.getToken",
            only_result=False,
            authCode=authCode,
            account=account,
            accountType=account_type,
        )
        if jo["code"] == 0:
            self.access_token = jo["result"]["accessToken"]
            self.refresh_token = jo["result"]["refreshToken"]
            if self.update_token_event_callback:
                self.update_token_event_callback(self.access_token, self.refresh_token)

        return jo

    async def async_refresh_token(self, refresh_token: str):
        """刷新访问令牌"""
        jo = await self._async_invoke_aqara_cloud_api(
            intent="config.auth.refreshToken",
            only_result=False,
            refreshToken=refresh_token,
        )
        if jo["code"] == 0:
            self.access_token = jo["result"]["accessToken"]
            self.refresh_token = jo["result"]["refreshToken"]
            if self.update_token_event_callback:
                self.update_token_event_callback(self.access_token, self.refresh_token)

        return jo

    async def async_query_device_sub_info(self, did: str):
        """获取设备入网bindKey"""
        return await self._async_invoke_aqara_cloud_api(
            intent="query.device.bindKey", did=did
        )

    async def async_query_device_info(
        self,
        dids: list = None,
        position_id: str = None,
        page_num: int = None,
        page_size: int = None,
    ):
        """查询设备信息"""
        resp = await self._async_invoke_aqara_cloud_api(
            intent="query.device.info",
            dids=dids,
            positionId=position_id,
            pageNum=page_num,
            pageSize=page_size,
        )
        if resp:
            return resp.get("data")
        return {}

    async def async_query_all_devices_info(self, page_size: int = 50):
        """查询所有设备信息"""
        continue_flag = True
        page_num = 1
        devices = []
        while continue_flag:
            jo = await self.async_query_device_info(
                page_num=page_num, page_size=page_size
            )
            devices.extend(jo)
            if len(jo) < page_size:
                continue_flag = False
            page_num = page_num + 1
        return devices

    async def async_query_device_sub_info(self, did: str):
        """查询网关下子设备信息"""
        return await self._async_invoke_aqara_cloud_api(
            intent="query.device.subInfo", did=did
        )

    async def async_query_resource_info(self, model: str, resource_id: str = None):
        """查询已开放的资源详情"""
        return await self._async_invoke_aqara_cloud_api(
            intent="query.resource.info", model=model, resourceId=resource_id
        )

    async def async_query_resource_value(self, subject_id: str, resource_ids: list):
        """查询资源信息"""
        return await self._async_invoke_aqara_cloud_api(
            intent="query.resource.value",
            resources=[{"subjectId": subject_id, "resourceIds": resource_ids}],
        )

    async def async_write_resource_device(
        self, subject_id: str, resource_id: str, value: str
    ):
        """控制设备"""
        return await self._async_invoke_aqara_cloud_api(
            intent="write.resource.device",
            list_data=True,
            subjectId=subject_id,
            resources=[{"resourceId": resource_id, "value": value}],
        )

    async def async_write_device_openconnect(
        self, subject_id: str
    ):
        """开启网关添加子设备模式"""
        return await self._async_invoke_aqara_cloud_api(
            intent="write.device.openConnect",
            resources=[{"subjectId": subject_id}]
        )

    async def async_write_device_closeconnect(
        self, subject_id: str
    ):
        """关闭网关添加子设备模式"""
        return await self._async_invoke_aqara_cloud_api(
            intent="write.device.closeConnect",
            resources=[{"subjectId": subject_id}]
        )

    async def async_subscribe_resources(
        self, subject_id: str, resource_ids: list, attach=None
    ):
        """订阅资源"""
        return await self._async_invoke_aqara_cloud_api(
            intent="config.resource.subscribe",
            resources=[{"subjectId": subject_id, "resourceIds": resource_ids, "attach": attach}],
        )

    async def async_unsubscribe_resources(
        self, subject_id: str, resource_ids: list, attach=None
    ):
        """取消订阅资源"""
        return await self._async_invoke_aqara_cloud_api(
            intent="config.resource.unsubscribe",
            resources=[{"subjectId": subject_id, "resourceIds": resource_ids, "attach": attach}],
        )

    async def async_write_ir_startlearn(
        self, subject_id: str, time_length=20
    ):
        """开启红外学习"""
        return await self._async_invoke_aqara_cloud_api(
            intent="write.ir.startLearn",
            resources=[{"subjectId": subject_id, "timeLength": time_length}]
        )

    async def async_write_ir_cancellearn(
        self, subject_id: str
    ):
        """取消开启红外学习"""
        return await self._async_invoke_aqara_cloud_api(
            intent="write.ir.cancelLearn",
            resources=[{"subjectId": subject_id}]
        )

    async def async_query_ir_learnresult(
        self, subject_id: str, keyid: str
    ):
        """查询红外学习结果"""
        return await self._async_invoke_aqara_cloud_api(
            intent="query.ir.learnResult",
            resources=[{"subjectId": subject_id, "keyId": keyid}]
        )
