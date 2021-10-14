import argparse
from nftninja.manager import Manager
import config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--edition", dest="edition", type=int, help="Edition number", default=1)
    parser.add_argument("-in", "--item-name", dest="item_name", help="Name of the items in metadata JSON", default="NFTNinja")
    parser.add_argument("-imax", "--items-max-number", dest="imax", type=int, help="Maximum number of items to generate", default=5)
    parser.add_argument("-rg", "--regenerate", dest="regenerate", action='store_true', help="Regegerate build folder")
    parser.add_argument("-nbi", "--no-build-images", dest="build_images", action='store_false', help="Build images")
    parser.add_argument("-nbm", "--no-build-metadata", dest="build_metadata", action='store_false', help="Build JSON metadata")
    parser.add_argument("-u", "--external-url", dest="external_url", help="External URL where images and metadata will be stored")
    parser.add_argument("-r", "--run", dest="run", action='store_true', help="Determines if NFTNinja can run or not. If it is not supplied, program will not generate any output")
    parser.add_argument("-g", "--generate-rarity-config", dest="generate_rarity_config", action='store_true', help="Generates rarity configuration template based on your configuration")
    parser.add_argument("-c", "--count-all-possibilities", dest="count_all_possibilities", action='store_true', help="Calculates all the possible combinations of your sprites based on your configuration")
    
    args = parser.parse_args()
    
    config.EDITION = args.edition
    config.ITEM_NAME = args.item_name
    config.MAX_ITEMS_TO_GENERATE = args.imax
    config.CLEAN_UP_BEFORE_GENERATE = args.regenerate
    config.GENERATE_IMAGES = args.build_images
    config.GENERATE_METADATA = args.build_metadata
    config.EXTERNAL_URL = args.external_url
    
    print(args)
    m = Manager(config)
    
    if args.generate_rarity_config:
        m.generate_rarity_config()
    if args.count_all_possibilities:
        m.count_all_possibilities()
    elif args.run:
        if args.regenerate:
            m.init_before_generate()
        m.generate_dnas()
        m.run()
