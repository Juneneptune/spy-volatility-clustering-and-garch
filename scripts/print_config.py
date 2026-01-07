from spy_volatility.utils.config import load_config, get_project_root

def main() -> None:

    config_name = "default.yaml"
    cfg = load_config(config_name)

    print("[print_config] Loaded configuration")
    print(f"Config file: {config_name}")
    print(f"Start date:  {cfg['data']['start_date']}")
    print(f"End date:    {cfg['data']['end_date']}")

if __name__ == "__main__":
    main()