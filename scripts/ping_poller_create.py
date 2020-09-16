import json

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()


class magnum_cache:
    def __init__(self, **kwargs):

        self.nature = "mag-1"
        self.cluster_ip = None
        self.edge_matches = []

        for key, value in kwargs.items():

            if ("host" in key) and value:
                self.host = value

            if ("nature" in key) and value:
                self.nature = value

            if ("cluster_ip" in key) and value:
                self.cluster_ip = value

            if ("edge_matches" in key) and value:
                self.edge_matches.extend(value)

        self.cache_url = "http://{}/proxy/insite/{}/api/-/model/magnum/{}".format(
            self.host, self.nature, self.cluster_ip
        )

        print(self.cache_url)

    def cache_fetch(self):

        response = requests.get(self.cache_url, verify=False, timeout=30.0)

        return json.loads(response.text)

    def catalog_cache(self):

        cache = self.cache_fetch()

        if cache:

            ipg_ip_db = []

            for device in cache["magnum"]["magnum-controlled-devices"]:

                if device["device"] in self.edge_matches:

                    ipg_ip_db.append(device["control-1-address"]["host"])

                    if device["device"] in ["EXE", "IPX"]:
                        ipg_ip_db.append(device["control-2-address"]["host"])

            print(len(ipg_ip_db))
            print(ipg_ip_db)


def main():

    params = {
        "host": "172.16.205.201",
        "nature": "mag-1",
        "cluster_ip": "100.103.224.21",
        "edge_matches": [
            "EXE",
            "IPX",
            "570IPG-X19-25G",
            "3067VIP10G-3G",
            "570ITXE",
            "570ASI-D",
            "5700MSC-IP",
            "570J2K",
            "570OIPG",
            "evBLADE-Z10-UDX-2",
            "7880IPG-NAT-6",
            "VUE-CUBE",
            "VUE-TOUCH-10",
        ],
    }

    collector = magnum_cache(**params)

    collector.catalog_cache()


if __name__ == "__main__":
    main()
