import argparse
from artengine.manager import Manager
import config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-cb", "--clean-build-folder", dest="clean_build_folder", action='store_true', help="Gegerate or regenerate build folder. Warning, it will remove all of your work")
    parser.add_argument("-g", "--generate-rarity-config", dest="generate_rarity_config", action='store_true', help="Generates rarity configuration template based on your configuration")
    parser.add_argument("-c", "--count-all-possibilities", dest="count_all_possibilities", action='store_true', help="Calculates all the possible combinations of your sprites based on your configuration")
    parser.add_argument("-cr", "--check-rarities", dest="check_rarities", action='store_true', help="Checks difference between defined rarity configurations and real rarities")
    

    args = parser.parse_args()
    print(args)
    print("-"*100)
    m = Manager(config)
    
    if args.clean_build_folder:
        m.init_before_generate()
    elif args.generate_rarity_config:
        m.generate_rarity_config()
    elif args.count_all_possibilities:
        m.count_all_possibilities()
    elif args.check_rarities:
        m.check_rarities()
