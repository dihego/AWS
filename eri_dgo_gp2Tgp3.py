import boto3
import logging
import sys
import os

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


def main(event, context):
    dry_run = True

    ec2 = boto3.Session(profile_name="ericgri").client("ec2")

    all_volumes = get_all_volumes(ec2)
    logger.info(f"Received a total of: {len(all_volumes)} volumes")

    applicable_volumes = filter_volumes(all_volumes)
    logger.info(f"Only {len(applicable_volumes)} volumes are applicable")

    for volume in applicable_volumes:
        logger.info(f"Modifying volume: {volume['VolumeId']}")
        modify_volume(ec2, volume["VolumeId"], dry_run)


def get_all_volumes(ec2):
    response = ec2.describe_volumes()
    results = response['Volumes']

    while "NextToken" in response:
        response = ec2.describe_volumes(NextToken=response["NextToken"])
        results.extend(response["Volumes"])

    return results


def filter_volumes(volume_list):
    results = []
    for volume in volume_list:
        if volume["State"] == "available" and volume["VolumeType"] == "gp2":
            results.append(volume)

    return results


def modify_volume(ec2, volume_id, dry_run):
    ec2.modify_volume(VolumeId=volume_id, VolumeType="gp3", DryRun=dry_run)


if __name__ == "__main__":
    main({}, None)
