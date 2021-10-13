from PIL import Image
import os, json
import random
import hashlib


nucleotides = [
    'background',
    'background2',
    'color',
    'body',
    'ear',
    'tail',
    'eye',
    'mouth',
    'foot'
]


colors = {
    'Yellowish': ['body', 'ear', 'tail'],
    'Greenish': ['body', 'ear', 'tail'],
}


nucleotide_options = {nucl: [os.path.splitext(x)[0] for x in os.listdir('./layers/single/' + nucl)] for nucl in nucleotides if nucl != 'color'}
nucleotide_options['color'] = ['Greenish', 'Yellowish']


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
    result = base_image.resize((600, 700))
    print(f"./build/Filemon-{id}.png")
    result.save(f"./build/Filemon-{id}.png")


def hash_dna(dna):
    return hashlib.sha1(json.dumps(dna, sort_keys=True).encode('UTF-8')).hexdigest()

def generate_metadata(id, dna):
    attributes = []
    for d in dna:
        attributes.append({'trait_type': d, 'value': dna[d]})

    metadata = {
        'dna': hash_dna(dna),
        'name': f'Filemon #{id}',
        'description': "Schrödinger's cat who wants to live",
        'image': 'ipfs://NewUriToReplace/1.png',
        'edition': 1,
        'date': '2021-10-13',
        'attributes': attributes,
        'engine': 'NFTNinja v0.1'
    }
    return metadata


dnas = []
existing_dna_hashes = []


if __name__ == "__main__":
    for d in range(100):
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
        scf = generate_sprite_config(dd)
        metadata = generate_metadata(idx, dd)
        with open(f'build/{idx}.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        build_image(idx, scf)
