"""Initializes a AdManagerClient using a Service Account."""

# Import necessary libraries
import sys

# adding Utils to the system path
sys.path.append("../")
sys.path.append("../../")
from googleads import ad_manager, errors
import config
import numpy as np
from Utils.json_tools import dump_to_json, read_from_json


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


def get_values_by_key(client, selected_key=""):
    print("Retrieving all available values for the selected targeting-key from the ad server...")
    service = client.GetService("CustomTargetingService", version=config.API_VERSION)

    targeting_data = read_from_json("../data/targeting_keys.json")
    key_as_id = ""

    for key in targeting_data:
        if key["name"] == selected_key:
            key_as_id = key["id"]

    statement = (
        ad_manager.StatementBuilder(version="v202308")
        .Where("customTargetingKeyId = :id")
        .WithBindVariable("id", key_as_id)
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
    json_path = "../data/" + str(key_as_id) + ".json"
    dump_to_json(all_values, json_path)
    return all_values


def get_values_by_id(client, key_id=""):
    print("Retrieving all available values for the selected targeting-id from the ad server...")
    service = client.GetService("CustomTargetingService", version=config.API_VERSION)
    
    statement = (
        ad_manager.StatementBuilder(version="v202308")
        .Where("customTargetingKeyId = :id")
        .WithBindVariable("id", key_id)
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
    json_path = "../data/" + str(key_id) + ".json"
    dump_to_json(all_values, json_path)
    return all_values
