from torch import nn
import torch
import re
from collections import Counter
from tensorflow.keras.preprocessing.sequence import pad_sequences


class SimpleModel(nn.Module):
    def __init__(self, num_tokens, emb_size=16, hid_size=64):
        super(self.__class__, self).__init__()
        self.emb = nn.Embedding(num_tokens, emb_size)
        self.dropout = nn.Dropout(p=0.5)
        self.lstm = nn.LSTM(emb_size, hid_size, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(2 * hid_size, 1)

    def forward(self, x):
        x = x.type(torch.LongTensor)
        emb = self.dropout(self.emb(x))
        h, _ = self.lstm(emb)
        estimate = self.fc(h[:, -1, :])
        return torch.flatten(estimate)


class Tokenizer:
    def __init__(self, data=None, maxlen=1024, mincount=3, params=None):
        if params is not None:
            self.maxlen = params['maxlen']
            self.mincount = params['mincount']
            self.w2i = params['w2i']
            self.i2w = params['i2w']
            self.num_tokens = len(self.w2i)
        else:
            self.maxlen = maxlen
            self.mincount = mincount
            text = ' '.join(data).lower()
            text = re.sub(r'[^\w\s]', '', text)
            words = dict(Counter((text.split())))
            words = {key for key, val in words.items() if val >= mincount}
            self.num_tokens = len(words) + 4
            self.w2i = {'<unk>': 0, '<BOS>': 1, '<EOS>': 2, '<pad>': 3}
            self.i2w = ['<unk', '<BOS>', '<EOS>', '<pad>']
            for w in words:
                self.w2i[w] = len(self.i2w)
                self.i2w.append(w)

    def tokenize(self, data):
        output = []
        for sent in data:
            text = re.sub(r'[^\w\s]', '', sent.lower())
            output.append([1])
            for w in text.split():
                if w in self.w2i:
                    output[-1].append(self.w2i[w])
                else:
                    output[-1].append(0)
            output[-1].append(2)
        return pad_sequences(output, maxlen=self.maxlen, value=3)

    def save(self, path):
        params = {'w2i': self.w2i, 'i2w': self.i2w, 'maxlen': self.maxlen, 'mincount': self.mincount}
        with open(path, 'w') as file:
            file.write(str(params))

    @staticmethod
    def load(path):
        with open(path) as file:
            d = eval(file.read())
            return Tokenizer(params=d)


class End2End:
    def __init__(self, tok_path='models/tokenizer.tok', model_path='models/regression.pt'):
        self.tokenizer = Tokenizer.load(tok_path)
        self.model = SimpleModel(self.tokenizer.num_tokens, 16, 32)
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.model.eval()

    def __call__(self, text):
        X = torch.LongTensor(self.tokenizer.tokenize([text]))
        y = torch.round(self.model(X))[0].item()
        if y > 10:
            y = 10
        elif y < 1:
            y = 1
        return y


class Handler:
    model = None
