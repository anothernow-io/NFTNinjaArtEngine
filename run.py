import argparse
from artengine.manager import Manager
import config


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--edition", dest="edition", type=int, help="Edition number", default=1)
    parser.add_argument("-in", "--item-name", dest="item_name", help="Name of the items in metadata JSON", default="AgentFUD")
    parser.add_argument("-imax", "--items-max-number", dest="imax", type=int, help="Maximum number of items to generate", default=5)
    parser.add_argument("-nbi", "--no-build-images", dest="build_images", action='store_false', help="Build images")
    parser.add_argument("-nbm", "--no-build-metadata", dest="build_metadata", action='store_false', help="Build JSON metadata")
    parser.add_argument("-u", "--external-url", dest="external_url", help="External URL where images and metadata will be stored")
    parser.add_argument("-cb", "--clean-build-folder", dest="clean_build_folder", action='store_true', help="Gegerate or regenerate build folder. Warning, it will remove all of your work")
    parser.add_argument("-r", "--run", dest="run", action='store_true', help="Determines if NFTNinja can run or not. If it is not supplied, program will not generate any output")
    

    args = parser.parse_args()
    
    config.EDITION = args.edition
    config.ITEM_NAME = args.item_name
    config.MAX_ITEMS_TO_GENERATE = args.imax
    config.GENERATE_IMAGES = args.build_images
    config.GENERATE_METADATA = args.build_metadata
    config.EXTERNAL_URL = args.external_url if args.external_url is not None else config.EXTERNAL_URL
    
    print(args)
    m = Manager(config)
    
    if args.run:
        if args.clean_build_folder:
            m.init_before_generate()
        m.generate_dnas()
        m.run()
