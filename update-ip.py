import requests, json, time, datetime, os

def abs_path():
    return os.path.dirname(os.path.realpath(__file__))


ENDPOINT = abs_path() + "/docs/index.json"
IP_LOG = abs_path() + "/docs/ip_log.json"
UPDATE_INTERVAL = 10  # seconds in-between checks


def json_to_dict(filename):
    with open(filename, encoding="utf-8") as f:
        if not f.read(1):
            return {}
        else:
            f.seek(0)
            return json.load(f)


def dict_to_json(filename, _dict):
    with open(filename, "w", encoding="utf-8") as f:
        return json.dump(_dict, f)

def append_ip_log_to_file(filename, _dict):
    ip_log = json_to_dict(filename)
    ip_log["ip_log"].insert(0, _dict)
    with open(filename, "w", encoding="utf-8") as f:
        return json.dump(ip_log, f)

def get_ip(endpoint):
    r = requests.get(endpoint)
    if r.status_code == 200: return r.json()["ip"]
    raise Exception("Unexpected error in api")


def get_served_version():
    return json_to_dict(ENDPOINT)


def get_current_version():
    return {"ipv4": get_ip("https://api.ipify.org/?format=json"),"checked": now().isoformat()}


def update_served(_new):
    # update the file
    dict_to_json(ENDPOINT, _new)
    append_ip_log_to_file(IP_LOG, _new)
    # deploy
    os.chdir(abs_path())
    os.system("git pull")
    os.system("git add '%s'" % ENDPOINT)
    os.system("git add '%s'" % IP_LOG)
    os.system('git commit -m "updated IP to %s at %s"' % (_new["ipv4"], now()))
    os.system("git push")

def now(): return datetime.datetime.now()


served = get_served_version()


def updated_if_needed():
    global served
    try: current = get_current_version()
    except Exception as e:
        print("[WARN] update failed at %s with error message: %s (will retry in %s seconds)" % (now(), e, UPDATE_INTERVAL))
        return
    if current["ipv4"] != served["ipv4"]:
        print("Updating [%s] to [%s] at %s..." % (served, current, now()), end="", flush=True)
        update_served(current)
        served = current
        print("DONE")


while True:
    updated_if_needed()
    time.sleep(UPDATE_INTERVAL)
