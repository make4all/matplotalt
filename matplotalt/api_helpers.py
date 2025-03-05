import os
import torch
from openai import OpenAI, AzureOpenAI

from matplotalt_helpers import gcf_as_pil_img

def get_openai_vision_response(api_key, prompt, base64_img, model="gpt-4-vision-preview", use_azure=False,
                               max_tokens=300, return_full_response=False):
    if use_azure:
        client = AzureOpenAI(api_key=api_key,
                             api_version=os.getenv("OPENAI_API_VERSION"),
                             base_url=os.getenv("AZURE_BASE_URL"))
                             #azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"))
    else:
        client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt},
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_img}",
                },
                },
            ],
            }
        ],
        max_tokens=max_tokens
    )
    if return_full_response:
        return response
    return response.choices[0].message.content


from transformers import AutoModel, AutoTokenizer

# Supports VLM and image-only models
def get_huggingface_model_response(model, prompt="", tokenizer=None, image=None, input_ids=None, imageonly=False, **kwargs):
    if not imageonly: # If this is a VLM
        if input_ids is None: # And we're not given input ids
            # We need to tokenize the given prompt
            if isinstance(tokenizer, str): # try loading tokenizer from name
                tokenizer = AutoTokenizer.from_pretrained(tokenizer)
            elif tokenizer is None and isinstance(model, str): # else try loading from model name
                tokenizer = AutoTokenizer.from_pretrained(model)
            elif tokenizer is None: # Switch to image only mode?
                raise ValueError("No tokenizer provided, if using an imageonly model, set imageonly=True")
            input_ids = tokenizer.batch_tokenize(prompt, return_tensors="pt").input_ids

    if isinstance(model, str): # Try to initialize using model name
        model = AutoModel.from_pretrained(model)
    if image is None:
        image = gcf_as_pil_img()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    if imageonly:
        outputs = model.generate(image.to(device), **kwargs)
    else:
        outputs = model.generate(image.to(device), input_ids=input_ids.to(device), **kwargs)

    return outputs




'''
from transformers import DonutProcessor, AutoModel, VisionEncoderDecoderModel, AutoConfig, AutoProcessor
from PIL import Image
import torch, os, re
from pprint import pprint


# Generation code from https://github.com/vis-nlp/UniChart
model_name = "ahmed-masry/unichart-chart2text-statista-960" #"ahmed-masry/unichart-base-960"

base_model = VisionEncoderDecoderModel.from_pretrained("ahmed-masry/unichart-base-960")
base_processor = AutoProcessor.from_pretrained("ahmed-masry/unichart-base-960")

statista_model = VisionEncoderDecoderModel.from_pretrained("ahmed-masry/unichart-chart2text-statista-960" )
statista_processor = AutoProcessor.from_pretrained("ahmed-masry/-chart2text-statista-960" )

pew_model = VisionEncoderDecoderModel.from_pretrained("ahmed-masry/unichart-chart2text-pew-960" )
pew_processor = AutoProcessor.from_pretrained("ahmed-masry/unichart-chart2text-pew-960" )
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def generate_summary(image_path, model, processor, input_prompt="<summarize_chart> <s_answer>"):
    model.to(device)
    image = Image.open(image_path).convert("RGB")
    decoder_input_ids = processor.tokenizer(input_prompt, add_special_tokens=False, return_tensors="pt").input_ids
    pixel_values = processor(image, return_tensors="pt").pixel_values

    outputs = model.generate(
        pixel_values.to(device),
        decoder_input_ids=decoder_input_ids.to(device),
        max_length=model.decoder.config.max_position_embeddings,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=4,
        bad_words_ids=[[processor.tokenizer.unk_token_id]],
        return_dict_in_generate=True,
    )
    sequence = processor.batch_decode(outputs.sequences)[0]
    sequence = sequence.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
    sequence = sequence.split("<s_answer>")[1].strip()
    pprint(sequence)
'''