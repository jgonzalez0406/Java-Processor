from flask import Flask, jsonify, request
import re
import torch
import tiktoken
from model import GPTConfig, GPT
import os
from contextlib import nullcontext

app = Flask(__name__)

def load_trained_model(items):
    init_from = 'resume'  # or specify the path to the model checkpoint
    out_dir = '/nublar/datasets/jm52m/'  # ignored if init_from is not 'resume'
    num_samples = 1
    max_new_tokens = 50
    temperature = 0.8
    top_k = 200
    seed = 1337
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    dtype = 'float16'
    compile_model = False

    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cuda.matmul.allow_tf32 = True  # allow tf32 on matmul
    torch.backends.cudnn.allow_tf32 = True  # allow tf32 on cudnn
    device_type = 'cuda' if 'cuda' in device else 'cpu'  # for later use in torch.autocast
    ptdtype = {'float32': torch.float, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
    ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)


    if init_from == 'resume':
        # Init from a model saved in a specific directory
      
        checkpoint = torch.load('/nublar/datasets/jm52m/ckpt_finetune.pt', map_location=device) #replace with location of checkpoint
        gptconf = GPTConfig(**checkpoint['model_args'])
        model = GPT(gptconf)
        state_dict = checkpoint['model']
        unwanted_prefix = '_orig_mod.'
        for k, v in list(state_dict.items()):
            if k.startswith(unwanted_prefix):
                state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
        model.load_state_dict(state_dict)
    elif init_from.startswith('gpt2'):
        # Init from a given GPT-2 model
        model = GPT.from_pretrained(init_from, dict(dropout=0.0))

    model.eval()
    model.to(device)
    if compile_model:
        model = torch.compile(model)
 enc = tiktoken.get_encoding("gpt2")
    encode = lambda s: enc.encode(s, allowed_special={""})
    decode = lambda l: enc.decode(l)


    #for item in items:
    input_ids = encode(items)
    input_tensor = torch.tensor(input_ids, dtype=torch.long, device=device)[None, ...]

    with torch.no_grad():
        with ctx:
            for k in range(num_samples):
                try:
                    y = model.generate(input_tensor, max_new_tokens, temperature=temperature, top_k=top_k)
                    ret = decode(y[0].tolist())
                    ret = re.search('(<s>.*</s>)', ret)
                    ret = ret.group(1)
                    ret = ret[:ret.find('<|endoftext|>')]
                    ret = ret.replace('<s>', '').replace('</s>', '')
                    ret = ret.replace('</s', '')
                    prediction = ret.strip()

                except:
                    prediction = ('none')

    return prediction

@app.route('/generate-description', methods=['POST'])
def generate_description():
    data = request.json
    method_text = data['method_text']

 method_description = load_trained_model(method_text)

    return jsonify({'method_description': method_description})



if __name__ == '__main__':
    app.run()
