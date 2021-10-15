import argparse
from artengine.manager import Manager
import config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", dest="init", action='store_true', help="Gegerate build folder")
    parser.add_argument("-rg", "--regenerate", dest="regenerate", action='store_true', help="Regegerate build folder")
    parser.add_argument("-g", "--generate-rarity-config", dest="generate_rarity_config", action='store_true', help="Generates rarity configuration template based on your configuration")
    parser.add_argument("-c", "--count-all-possibilities", dest="count_all_possibilities", action='store_true', help="Calculates all the possible combinations of your sprites based on your configuration")
    parser.add_argument("-cr", "--check-rarities", dest="check_rarities", action='store_true', help="Checks difference between defined rarity configurations and real rarities")
    

    args = parser.parse_args()
    
    print(args)
    m = Manager(config)
    
    if args.init:
        m.init_before_generate()
    elif args.generate_rarity_config:
        m.generate_rarity_config()
    elif args.count_all_possibilities:
        m.count_all_possibilities()
    elif args.check_rarities:
        m.check_rarities()
