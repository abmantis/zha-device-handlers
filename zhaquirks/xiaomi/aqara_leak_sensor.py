from zigpy.profiles import PROFILES, zha
from zigpy.zcl.clusters.general import Basic, PowerConfiguration, Identify, Ota
from zigpy.zcl.clusters.security import IasZone
from zigpy import quirks
from zigpy.quirks.xiaomi import AqaraWaterSensor
from zhaquirks.xiaomi import BasicCluster, PowerConfigurationCluster,\
    TemperatureMeasurementCluster, XiaomiCustomDevice
from zhaquirks import LocalDataCluster

#  remove the zigpy version of this device handler
if AqaraWaterSensor in quirks._DEVICE_REGISTRY:
    quirks._DEVICE_REGISTRY.remove(AqaraWaterSensor)


class AqaraLeakSensor(XiaomiCustomDevice):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class MotionCluster(LocalDataCluster, IasZone):
        cluster_id = IasZone.cluster_id
        ZONE_TYPE = 0x0001
        LEAK_TYPE = 0x002a

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._update_attribute(self.ZONE_TYPE, self.LEAK_TYPE)

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=1026
        #  device_version=1
        #  input_clusters=[0, 3, 1]
        #  output_clusters=[25]>
        1: {
            'profile_id': zha.PROFILE_ID,
            'device_type': zha.DeviceType.IAS_ZONE,
            'input_clusters': [
                BasicCluster.cluster_id,
                Identify.cluster_id,
                PowerConfigurationCluster.cluster_id,
            ],
            'output_clusters': [
                Ota.cluster_id
            ],
        },
    }

    replacement = {
        'endpoints': {
            1: {
                'manufacturer': 'LUMI',
                'model': 'lumi.sensor_wleak.aq1',
                'input_clusters': [
                    BasicCluster,
                    Identify.cluster_id,
                    PowerConfigurationCluster,
                    TemperatureMeasurementCluster,
                    MotionCluster
                ],
            }
        },
    }
