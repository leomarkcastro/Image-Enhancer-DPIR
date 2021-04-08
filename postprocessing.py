from main_dpir_deblur import deblur
from main_dpir_denoising import denoising
from main_dpir_sisr_real_applications import sisr

import sys
import json
import secrets
import shutil

template = {
    "source": [],
    "result": [],
    "job": [
        {
            "type": "deblur",
            "denoise_level": 7.65/255.0, 
            "model_to_use": 'drunet_color'
        },
        {
            "type": "denoise",
            "denoise": 200, 
            "model_to_use": "drunet_color"
        },
        {
            "type": "resize",
            "denoise": 0,
            "scale": [2], 
            "model_to_use": "drunet_color"
        }
    ]
}

if __name__ == "__main__":

    to_parse = sys.argv[1]

    with open(to_parse) as fp:
        template = json.load(fp)
    
    point_a = template["source"]
    point_b = ["_temp", f"job_{secrets.token_hex(8)}"]

    todelete = []

    # Do the job queue

    for ij, job in enumerate(template["job"]):

        print(f"\n\nDoing job task [{ij+1}/{len(template['job'])}]\n\n")

        todelete.append(point_b)

        print("Source: ", point_a)
        print("Destination: ", point_b)
        print()

        if job["type"] == "deblur":
            deblur(point_a, point_b, job["denoise_level"], job["model_to_use"])

        elif job["type"] == "denoise":
            denoising(point_a, point_b, job["denoise"], job["model_to_use"])

        elif job["type"] == "resize":
            sisr(point_a, point_b, job["denoise"], job["scale"] ,job["model_to_use"])

        point_a = point_b[:]
        
        if ij+2 == len(template['job']):
            point_b = template["result"]
        else:
            point_b = ["_temp", f"job_{secrets.token_hex(8)}"]
    
    print("\n\n" + "="*20 + "\n\nEND OF PROCESS")
    # Delete the temporary files

    for loc in todelete[:-1]:
        shutil.rmtree("/".join(loc))
    
    print("Cleaned cache images")