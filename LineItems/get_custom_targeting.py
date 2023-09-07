"""Initializes a AdManagerClient using a Service Account."""

# Import necessary libraries
import sys

# adding Utils to the system path
sys.path.append("../")
sys.path.append("../../")
from googleads import ad_manager, errors
import config
import numpy as np
from Utils.json_tools import dump_to_json


def main(client):
    get_all_targeting_keys(client)
    get_values_by_key(client, id=665461)


def get_all_targeting_keys(client):
    service = client.GetService("CustomTargetingService", version=config.API_VERSION)

    statement = (
        ad_manager.StatementBuilder(version=config.API_VERSION)
        .Where("status LIKE :status")
        .WithBindVariable("status", "ACTIVE")
    )
    all_keys = []

    while True:
        response = service.getCustomTargetingKeysByStatement(statement.ToStatement())
        if "results" in response and len(response["results"]):
            for key in response["results"]:
                entry = {
                    "name": key["name"],
                    "id": key["id"],
                }
                all_keys.append(entry)
                statement.offset += statement.limit
        else:
            break
    dump_to_json(all_keys, "../data/targeting_keys.json")


def get_values_by_key(client, key="", id=0):
    service = client.GetService("CustomTargetingService", version=config.API_VERSION)

    statement = (
        ad_manager.StatementBuilder(version="v202308")
        .Where("customTargetingKeyId = :id")
        .WithBindVariable("id", id)
    )

    all_values = []

    while True:
        response = service.getCustomTargetingValuesByStatement(statement.ToStatement())
        if "results" in response and len(response["results"]):
            for value in response["results"]:
                entry = {
                    "name": value["name"],
                    "id": value["id"],
                }
                all_values.append(entry)
                statement.offset += statement.limit
        else:
            break
    dump_to_json(all_values, "../data/hb_bidders.json")


if __name__ == "__main__":
    client = ad_manager.AdManagerClient.LoadFromStorage()
    main(client)
