import shutil, os, hashlib, json
from PIL import Image
from typing import List
from time import strftime, gmtime
import random

class Manager:
    def __init__(self, config) -> None:
        self.config = config
        self.dnas = []
        self.existing_dna_hashes = []
        self.nucleotide_options = {nucl: [os.path.splitext(x)[0] for x in os.listdir('./layers/single/' + nucl)] for nucl in self.config.nucleotides if nucl != 'color'}
        self.nucleotide_options['color'] = self.config.AVAILABLE_COLORS

    def init_before_generate(self):
        if not self.config.CLEAN_UP_BEFORE_GENERATE:
            return
        if os.path.exists('./build'):
            print("Removing bulid folder ...")
            shutil.rmtree('./build')
        print("Creating build folder ...")
        os.mkdir('./build')
        os.mkdir('./build/images')
        os.mkdir('./build/metadata')

    def hash_dna(self, dna):
        """
        Hash of a DNA
        """
        return hashlib.sha1(json.dumps(dna, sort_keys=True).encode('UTF-8')).hexdigest()

    def generate_sprite_config(self, dna):
        """
        Generates sprite config from a DNA
        """
        ret = []
        for ncl_name, ncl_value in dna.items():
            if ncl_name == 'color':
                for nucl in self.config.colors[ncl_value]:
                    img_name = dna[nucl]
                    ret.append([ncl_name, f'./layers/colors/{ncl_value}/{nucl}/{img_name}.png'])
            else:
                ret.append([ncl_name, f'./layers/single/{ncl_name}/{ncl_value}.png'])
        return ret

    def build_image(self, id: int, sprite_config: List):
        """
        Generating image and saving it to a target directory
        """
        base_image = Image.open('./layers/single/background/Pink.png')
        for i, sprite in enumerate(sprite_config):
            next_image = Image.open(sprite[1])
            base_image.paste(next_image, (0, 0), next_image)
        result = base_image.resize(self.config.IMAGE_SIZE)
        print(f"./build/images/{id}.png")
        result.save(f"./build/images/{id}.png")

    def build_metadata(self, id: int, dna: List):
        """
        Generating metadata from DNA
        """
        attributes = []
        for d in dna:
            attributes.append({'trait_type': d, 'value': dna[d]})

        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        metadata = {
            'dna': self.hash_dna(dna),
            'name': f'{self.config.ITEM_NAME} #{id}',
            'description': "Schrödinger's cat who wants to live",
            'image': f'{self.config.EXTERNAL_URL}/images/{id}.png',
            'edition': f'{self.config.EDITION}',
            'date': f'{date}',
            'attributes': attributes,
            'engine': 'Agent FUD Art Engine v0.1'
        }
        return metadata

    def generate_dnas(self):
        use_rarity_config = True
        try:
            with open(self.config.RARITY_JSON_NAME, "r") as file:
                rarities = json.load(file)
        except FileNotFoundError:
            use_rarity_config = False

        for d in range(self.config.MAX_ITEMS_TO_GENERATE):
            dnax = {}
            for n in self.config.nucleotides:
                if use_rarity_config:
                    dnax[n] = random.choices(self.nucleotide_options[n], weights=rarities[n].values(), k=1)[0]
                else:
                    dnax[n] = self.nucleotide_options[n][random.randint(0, len(self.nucleotide_options[n]) - 1)]
            h = self.hash_dna(dnax)
            if h in self.existing_dna_hashes:
                print("DNA exists, skipping...")
            else:
                self.existing_dna_hashes.append(h)
                self.dnas.append(dnax)
        print(f'Will generate {len(self.dnas)} art pieces.')

    def generate_rarity_config(self):
        print("Generating rarity configuration")
        rarity_config = {}
        for nucleotide in self.nucleotide_options:
            rarity_config[nucleotide] = {}
            for gene in self.nucleotide_options[nucleotide]:
                rarity_config[nucleotide][gene] = 1

        with open(self.config.RARITY_JSON_NAME, 'w', encoding='utf-8') as f:
            json.dump(rarity_config, f, ensure_ascii=False, indent=4)
        print("Done...")

    def count_all_possibilities(self):
        pass

    def check_rarities(self):
        pass

    def run(self):
        for idx, dd in enumerate(self.dnas, start=1):
            if self.config.GENERATE_METADATA:
                metadata = self.build_metadata(idx, dd)
                with open(f'build/metadata/{idx}.json', 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, ensure_ascii=False, indent=4)
            if self.config.GENERATE_IMAGES:
                scf = self.generate_sprite_config(dd)
                self.build_image(idx, scf)
