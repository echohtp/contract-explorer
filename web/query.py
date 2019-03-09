from google.cloud import bigquery
import json
import eth_utils
import pandas as pd
# import numpy as np

client = bigquery.Client()

def get_functions(contract_address):
    adrstr=eth_utils.to_checksum_address(contract_address)
    q = f"""
      SELECT *
      FROM `contract-explorer-233919.ethparis.functions4`
      WHERE addr='{adrstr}'
      """
    query_job = client.query(q)
    results = query_job.result()
    return results.to_dataframe().to_dict('records')

def get_functions_w_count(contract_address):
    adrstr=eth_utils.to_checksum_address(contract_address)
    q = f"""
    SELECT
        tree_hash,
        name,
        `hash`,
        count(DISTINCT addr) found_count
    FROM `contract-explorer-233919.ethparis.functions4`
    WHERE tree_hash IN (SELECT tree_hash FROM `contract-explorer-233919.ethparis.functions4` WHERE addr='{adrstr}')
    GROUP BY tree_hash, name, `hash`
    ORDER BY found_count DESC
    """
    query_job = client.query(q)
    results = query_job.result()
    return results.to_dataframe().to_dict('records')
