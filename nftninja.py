from PIL import Image
import os, json
import random
import hashlib
import shutil
from time import strftime, gmtime
from config import nucleotides, colors, AVAILABLE_COLORS, ITEM_NAME, IMAGE_SIZE
from config import MAX_ITEMS_TO_GENERATE, GENERATE_METADATA, GENERATE_IMAGES
from config import CLEAN_UP_BEFORE_GENERATE, EXTERNAL_URL, EDITION


nucleotide_options = {nucl: [os.path.splitext(x)[0] for x in os.listdir('./layers/single/' + nucl)] for nucl in nucleotides if nucl != 'color'}
nucleotide_options['color'] = AVAILABLE_COLORS


def generate_sprite_config(dna):
    ret = []
    for ncl_name, ncl_value in dna.items():
        if ncl_name == 'color':
            for nucl in colors[ncl_value]:
                img_name = dna[nucl]
                ret.append([ncl_name, f'./layers/colors/{ncl_value}/{nucl}/{img_name}.png'])
        else:
            ret.append([ncl_name, f'./layers/single/{ncl_name}/{ncl_value}.png'])
    return ret


def build_image(id, sprite_config):
    base_image = Image.open('./layers/single/background/Pink.png')
    for i, sprite in enumerate(sprite_config):
        next_image = Image.open(sprite[1])
        base_image.paste(next_image, (0, 0), next_image)
    result = base_image.resize(IMAGE_SIZE)
    print(f"./build/{ITEM_NAME}-{id}.png")
    result.save(f"./build/images/{ITEM_NAME}-{id}.png")


def hash_dna(dna):
    return hashlib.sha1(json.dumps(dna, sort_keys=True).encode('UTF-8')).hexdigest()

def generate_metadata(id, dna):
    attributes = []
    for d in dna:
        attributes.append({'trait_type': d, 'value': dna[d]})

    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    metadata = {
        'dna': hash_dna(dna),
        'name': f'{ITEM_NAME} #{id}',
        'description': "Schrödinger's cat who wants to live",
        'image': f'{EXTERNAL_URL}/images/{id}.png',
        'edition': f'{EDITION}',
        'date': f'{date}',
        'attributes': attributes,
        'engine': 'NFTNinja v0.1'
    }
    return metadata

def init_before_generate():
    if not CLEAN_UP_BEFORE_GENERATE:
        return
    if os.path.exists('./build'):
        print("Removing bulid folder ...")
        shutil.rmtree('./build')
    print("Creating build folder ...")
    os.mkdir('./build')
    os.mkdir('./build/images')
    os.mkdir('./build/metadata')

dnas = []
existing_dna_hashes = []


if __name__ == "__main__":
    init_before_generate()
    for d in range(MAX_ITEMS_TO_GENERATE):
        dnax = {}
        for n in nucleotides:
            dnax[n] = nucleotide_options[n][random.randint(0, len(nucleotide_options[n]) - 1)]
        h = hash_dna(dnax)
        if h in existing_dna_hashes:
            print("DNA exists, skipping...")
        else:
            existing_dna_hashes.append(h)
            dnas.append(dnax)
    for idx, dd in enumerate(dnas):
        if GENERATE_METADATA:
            metadata = generate_metadata(idx, dd)
            with open(f'build/metadata/{idx}.json', 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
        if GENERATE_IMAGES:
            scf = generate_sprite_config(dd)
            build_image(idx, scf)
