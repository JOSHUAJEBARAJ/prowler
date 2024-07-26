from unittest import mock

from prowler.providers.aws.services.dms.dms_service import RepInstance
from tests.providers.aws.utils import AWS_ACCOUNT_NUMBER, AWS_REGION_US_EAST_1

DMS_INSTANCE_NAME = "rep-instance"
DMS_INSTANCE_ARN = (
    f"arn:aws:dms:{AWS_REGION_US_EAST_1}:{AWS_ACCOUNT_NUMBER}:rep:{DMS_INSTANCE_NAME}"
)
KMS_KEY_ID = f"arn:aws:kms:{AWS_REGION_US_EAST_1}:{AWS_ACCOUNT_NUMBER}:key/abcdabcd-1234-abcd-1234-abcdabcdabcd"


class Test_dms_instance_multi_az:
    def test_dms_no_instances(self):
        dms_client = mock.MagicMock
        dms_client.instances = []

        with mock.patch(
            "prowler.providers.aws.services.dms.dms_service.DMS",
            new=dms_client,
        ):
            from prowler.providers.aws.services.dms.dms_instance_multi_az_enabled.dms_instance_multi_az_enabled import (
                dms_instance_multi_az_enabled,
            )

            check = dms_instance_multi_az_enabled()
            result = check.execute()
            assert len(result) == 0

    def test_dms_instance_multi_az_not_enabled(self):
        dms_client = mock.MagicMock
        dms_client.instances = []
        dms_client.instances.append(
            RepInstance(
                id=DMS_INSTANCE_NAME,
                arn=DMS_INSTANCE_ARN,
                status="available",
                public=True,
                kms_key=KMS_KEY_ID,
                auto_minor_version_upgrade=False,
                multi_az=False,
                region=AWS_REGION_US_EAST_1,
            )
        )

        with mock.patch(
            "prowler.providers.aws.services.dms.dms_service.DMS",
            new=dms_client,
        ):
            from prowler.providers.aws.services.dms.dms_instance_multi_az_enabled.dms_instance_multi_az_enabled import (
                dms_instance_multi_az_enabled,
            )

            check = dms_instance_multi_az_enabled()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"DMS Replication Instance {DMS_INSTANCE_NAME} does not have multi az enabled."
            )
            assert result[0].region == AWS_REGION_US_EAST_1
            assert result[0].resource_id == DMS_INSTANCE_NAME
            assert result[0].resource_arn == DMS_INSTANCE_ARN

    def test_dms_instance_multi_az_enabled(self):
        dms_client = mock.MagicMock
        dms_client.instances = []
        dms_client.instances.append(
            RepInstance(
                id=DMS_INSTANCE_NAME,
                arn=DMS_INSTANCE_ARN,
                status="available",
                public=True,
                kms_key=KMS_KEY_ID,
                auto_minor_version_upgrade=True,
                multi_az=True,
                region=AWS_REGION_US_EAST_1,
            )
        )

        with mock.patch(
            "prowler.providers.aws.services.dms.dms_service.DMS",
            new=dms_client,
        ):
            from prowler.providers.aws.services.dms.dms_instance_multi_az_enabled.dms_instance_multi_az_enabled import (
                dms_instance_multi_az_enabled,
            )

            check = dms_instance_multi_az_enabled()
            result = check.execute()
            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"DMS Replication Instance {DMS_INSTANCE_NAME} has multi az enabled."
            )
            assert result[0].region == AWS_REGION_US_EAST_1
            assert result[0].resource_id == DMS_INSTANCE_NAME
            assert result[0].resource_arn == DMS_INSTANCE_ARN
