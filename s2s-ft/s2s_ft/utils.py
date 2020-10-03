from __future__ import absolute_import, division, print_function

import logging
import os
import json
import random
import glob
import torch
import tqdm
import torch.utils.data


logger = logging.getLogger(__name__)

class RetrievalSeq2seqDatasetForBert(torch.utils.data.Dataset):
    def __init__(
            self, features, max_source_len, max_target_len,
            vocab_size, cls_id, sep_id, pad_id, mask_id,
            random_prob, keep_prob, offset, num_training_instances, 
            span_len=1, span_prob=1.0):
        self.features = features
        self.max_source_len = max_source_len
        self.max_target_len = max_target_len
        self.offset = offset
        if offset > 0:
            logger.info("  ****  Set offset %d in Seq2seqDatasetForBert ****  ", offset)
        self.cls_id = cls_id
        self.sep_id = sep_id
        self.pad_id = pad_id
        self.random_prob = random_prob
        self.keep_prob = keep_prob
        self.mask_id = mask_id
        self.vocab_size = vocab_size
        self.num_training_instances = num_training_instances
        self.span_len = span_len
        self.span_prob = span_prob

    def __len__(self):
        return int(self.num_training_instances)

    def __trunk(self, ids, max_len):
        if len(ids) > max_len - 1:
            ids = ids[:max_len - 1]
        ids = ids + [self.sep_id]
        return ids

    def __pad(self, ids, max_len):
        if len(ids) < max_len:
            return ids + [self.pad_id] * (max_len - len(ids))
        else:
            assert len(ids) == max_len
            return ids

    def __getitem__(self, idx):
        idx = (self.offset + idx) % len(self.features)
        feature = self.features[idx]
        source_ids = self.__trunk([self.cls_id] + feature["source_ids"], self.max_source_len)
        target_ids = self.__trunk(feature["target_ids"], self.max_target_len)
        # pseudo_ids = []
        # for tk_id in target_ids:
        #     p = random.random()
        #     if p < self.keep_prob:
        #         pseudo_ids.append(tk_id)
        #     elif p < self.keep_prob + self.random_prob:
        #         pseudo_ids.append(random.randint(0, self.vocab_size - 1))
        #     else:
        #         pseudo_ids.append(self.mask_id)

        num_source_tokens = len(source_ids)
        num_target_tokens = len(target_ids)

        source_ids = self.__pad(source_ids, self.max_source_len)
        target_ids = self.__pad(target_ids, self.max_target_len)
        # pseudo_ids = self.__pad(pseudo_ids, self.max_target_len)

        # if self.span_len > 1:
        #     span_ids = []
        #     span_id = 1
        #     while len(span_ids) < num_target_tokens:
        #         p = random.random()
        #         if p < self.span_prob:
        #             span_len = random.randint(2, self.span_len)
        #             span_len = min(span_len, num_target_tokens - len(span_ids))
        #         else:
        #             span_len = 1
        #         span_ids.extend([span_id] * span_len)
        #         span_id += 1
        #     span_ids = self.__pad(span_ids, self.max_target_len)
        #     return source_ids, target_ids, pseudo_ids, num_source_tokens, num_target_tokens, span_ids
        
        return source_ids, target_ids, num_source_tokens, num_target_tokens


class RetrievalSeq2seqDocDatasetForBert(torch.utils.data.Dataset):
    def __init__(
            self, features, max_source_len, max_target_len,
            vocab_size, cls_id, sep_id, pad_id, mask_id,
            random_prob, keep_prob, offset, num_training_instances, 
            span_len=1, span_prob=1.0):
        self.features = features
        self.max_source_len = max_source_len
        self.max_target_len = max_target_len
        self.offset = offset
        if offset > 0:
            logger.info("  ****  Set offset %d in Seq2seqDatasetForBert ****  ", offset)
        self.cls_id = cls_id
        self.sep_id = sep_id
        self.pad_id = pad_id
        self.random_prob = random_prob
        self.keep_prob = keep_prob
        self.mask_id = mask_id
        self.vocab_size = vocab_size
        self.num_training_instances = num_training_instances
        self.span_len = span_len
        self.span_prob = span_prob

    def __len__(self):
        return len(self.features)

    def __trunk(self, ids, max_len):
        if len(ids) > max_len - 1:
            ids = ids[:max_len - 1]
        ids = ids + [self.sep_id]
        return ids

    def __pad(self, ids, max_len):
        if len(ids) < max_len:
            return ids + [self.pad_id] * (max_len - len(ids))
        else:
            assert len(ids) == max_len
            return ids

    def __getitem__(self, idx):
        idx = (self.offset + idx) % len(self.features)
        feature = self.features[idx]
        source_ids = self.__trunk([self.cls_id] + feature["input_ids"], self.max_source_len)
        target_ids = self.__trunk([self.cls_id] + [0], self.max_source_len)
        source_ids = self.__pad(source_ids, self.max_source_len)
        target_ids = self.__pad(target_ids, self.max_target_len)
        return source_ids, target_ids

class Seq2seqDatasetForBert(torch.utils.data.Dataset):
    def __init__(
            self, features, max_source_len, max_target_len,
            vocab_size, cls_id, sep_id, pad_id, mask_id,
            random_prob, keep_prob, offset, num_training_instances, 
            span_len=1, span_prob=1.0):
        self.features = features
        self.max_source_len = max_source_len
        self.max_target_len = max_target_len
        self.offset = offset
        if offset > 0:
            logger.info("  ****  Set offset %d in Seq2seqDatasetForBert ****  ", offset)
        self.cls_id = cls_id
        self.sep_id = sep_id
        self.pad_id = pad_id
        self.random_prob = random_prob
        self.keep_prob = keep_prob
        self.mask_id = mask_id
        self.vocab_size = vocab_size
        self.num_training_instances = num_training_instances
        self.span_len = span_len
        self.span_prob = span_prob

    def __len__(self):
        return int(self.num_training_instances)

    def __trunk(self, ids, max_len):
        if len(ids) > max_len - 1:
            ids = ids[:max_len - 1]
        ids = ids + [self.sep_id]
        return ids

    def __pad(self, ids, max_len):
        if len(ids) < max_len:
            return ids + [self.pad_id] * (max_len - len(ids))
        else:
            assert len(ids) == max_len
            return ids

    def __getitem__(self, idx):
        idx = (self.offset + idx) % len(self.features)
        feature = self.features[idx]
        source_ids = self.__trunk([self.cls_id] + feature["source_ids"], self.max_source_len)
        target_ids = self.__trunk(feature["target_ids"], self.max_target_len)
        pseudo_ids = []
        for tk_id in target_ids:
            p = random.random()
            if p < self.keep_prob:
                pseudo_ids.append(tk_id)
            elif p < self.keep_prob + self.random_prob:
                pseudo_ids.append(random.randint(0, self.vocab_size - 1))
            else:
                pseudo_ids.append(self.mask_id)

        num_source_tokens = len(source_ids)
        num_target_tokens = len(target_ids)

        source_ids = self.__pad(source_ids, self.max_source_len)
        target_ids = self.__pad(target_ids, self.max_target_len)
        pseudo_ids = self.__pad(pseudo_ids, self.max_target_len)

        if self.span_len > 1:
            span_ids = []
            span_id = 1
            while len(span_ids) < num_target_tokens:
                p = random.random()
                if p < self.span_prob:
                    span_len = random.randint(2, self.span_len)
                    span_len = min(span_len, num_target_tokens - len(span_ids))
                else:
                    span_len = 1
                span_ids.extend([span_id] * span_len)
                span_id += 1
            span_ids = self.__pad(span_ids, self.max_target_len)
            return source_ids, target_ids, pseudo_ids, num_source_tokens, num_target_tokens, span_ids
        else:
            return source_ids, target_ids, pseudo_ids, num_source_tokens, num_target_tokens


def batch_list_to_batch_tensors(batch):
    batch_tensors = []
    for x in zip(*batch):
        if isinstance(x[0], torch.Tensor):
            batch_tensors.append(torch.stack(x))
        else:
            batch_tensors.append(torch.tensor(x, dtype=torch.long))
    return batch_tensors


def get_max_epoch_model(output_dir):
    fn_model_list = glob.glob(os.path.join(output_dir, "model.*.bin"))
    fn_optim_list = glob.glob(os.path.join(output_dir, "optim.*.bin"))
    if (not fn_model_list) or (not fn_optim_list):
        return None
    os.path.basename(output_dir)
    both_set = set([int(os.path.basename(fn).split('.')[1]) for fn in fn_model_list]
                   ) & set([int(os.path.basename(fn).split('.')[1]) for fn in fn_optim_list])
    if both_set:
        return max(both_set)
    else:
        return None


def load_and_cache_examples(
        example_file, tokenizer, local_rank, cached_features_file, shuffle=True):
    # Make sure only the first process in distributed training process the dataset, and the others will use the cache
    if local_rank not in [-1, 0]:
        torch.distributed.barrier()

    if cached_features_file is not None and os.path.exists(cached_features_file):
        logger.info("Loading features from cached file %s", cached_features_file)
        features = torch.load(cached_features_file)
    else:
        logger.info("Creating features from dataset file at %s", example_file)

        examples = []
        with open(example_file, mode="r", encoding="utf-8") as reader:
            for line in reader:
                examples.append(json.loads(line))
        features = []

        for example in tqdm.tqdm(examples):
            if isinstance(example["src"], list):
                source_tokens = example["src"]
                target_tokens = example["tgt"]
            else:
                source_tokens = tokenizer.tokenize(example["src"])
                target_tokens = tokenizer.tokenize(example["tgt"])
            features.append({
                    "source_ids": tokenizer.convert_tokens_to_ids(source_tokens),
                    "target_ids": tokenizer.convert_tokens_to_ids(target_tokens),
                })

        if shuffle:
            random.shuffle(features)

        if local_rank in [-1, 0] and cached_features_file is not None:
            logger.info("Saving features into cached file %s", cached_features_file)
            torch.save(features, cached_features_file)

    # Make sure only the first process in distributed training process the dataset, and the others will use the cache
    if local_rank == 0:
        torch.distributed.barrier()

    return features

def load_and_cache_doc_examples(example_file, tokenizer, local_rank, cached_doc_features_file):
    # Make sure only the first process in distributed training process the dataset, and the others will use the cache
    if local_rank not in [-1, 0]:
        torch.distributed.barrier()

    if cached_doc_features_file is not None and os.path.exists(cached_doc_features_file):
        logger.info("Loading features from cached file %s", cached_doc_features_file)
        features = torch.load(cached_doc_features_file)
    else:
        logger.info("Creating features from dataset file at %s", example_file)

        examples = []
        with open(example_file, mode="r", encoding="utf-8") as reader:
            for line in reader:
                examples.append(line.strip())
        features = []

        for example in tqdm.tqdm(examples):
            tokens = tokenizer.tokenize(example)
            features.append({
                    "input_ids":tokenizer.convert_tokens_to_ids(tokens)
                })

        if local_rank in [-1, 0] and cached_doc_features_file is not None:
            logger.info("Saving features into cached file %s", cached_doc_features_file)
            torch.save(features, cached_doc_features_file)

    # Make sure only the first process in distributed training process the dataset, and the others will use the cache
    if local_rank == 0:
        torch.distributed.barrier()

    return features

class Concator:
    '''
    concate query features and document features after retrieval
    '''
    def __init__(
            self, max_source_len, max_target_len,
            vocab_size, cls_id, sep_id, pad_id, mask_id,
            random_prob, keep_prob, offset, num_training_instances, 
            span_len=1, span_prob=1.0):
        self.max_source_len = max_source_len
        self.max_target_len = max_target_len
        self.offset = offset
        if offset > 0:
            logger.info("  ****  Set offset %d in Seq2seqDatasetForBert ****  ", offset)
        self.cls_id = cls_id
        self.sep_id = sep_id
        self.pad_id = pad_id
        self.random_prob = random_prob
        self.keep_prob = keep_prob
        self.mask_id = mask_id
        self.vocab_size = vocab_size
        self.num_training_instances = num_training_instances
        self.span_len = span_len
        self.span_prob = span_prob
    def __len__(self):
        return int(self.num_training_instances)
    
    def __trunk(self, ids, max_len):
        if len(ids) > max_len - 1:
            ids = ids[:max_len - 1]
        ids = ids + [self.sep_id]
        return ids

    def __pad(self, ids, max_len):
        if len(ids) < max_len:
            return ids + [self.pad_id] * (max_len - len(ids))
        else:
            assert len(ids) == max_len
            return ids
    
    def concate(self, query_ids, documents_ids, target_ids, num_source_tokens, num_target_tokens):
        new_source_ids = []
        new_target_ids = []
        new_pseudo_ids = []
        num_source_tokens = []
        num_target_tokens = []
        new_span_ids = []
        for query_id, documents_id, target_id, num_src_tokens, num_tgt_tokens in zip(query_ids, documents_ids, target_ids, num_source_tokens, num_target_tokens):
            query_ids = query_ids[:num_src_tokens]
            target_id = target_id[:num_tgt_tokens]
            for d_id in documents_id:
                s_ids = self.__trunk([self.cls_id] + query_id + d_id, self.max_source_len)
                t_ids = self._trunk(target_id, self.max_target_len)
                pseudo_ids = []
                for tk_id in target_ids:
                    p = random.random()
                    if p < self.keep_prob:
                        pseudo_ids.append(tk_id)
                    elif p < self.keep_prob + self.random_prob:
                        pseudo_ids.append(random.randint(0, self.vocab_size - 1))
                    else:
                        pseudo_ids.append(self.mask_id)
                num_source_tokens.append(len(s_ids))
                num_target_tokens.append(len(t_ids))

                src_ids = self.__pad(s_ids, self.max_source_len)
                tgt_ids = self.__pad(t_ids, self.max_target_len)
                pseudo_ids = self.__pad(pseudo_ids, self.max_target_len)

                if self.span_len > 1:
                    span_ids = []
                    span_id = 1
                    while len(span_ids) < len(t_ids):
                        p = random.random()
                        if p < self.span_prob:
                            span_len = random.randint(2, self.span_len)
                            span_len = min(span_len, len(t_ids) - len(span_ids))
                        else:
                            span_len = 1
                        span_ids.extend([span_id] * span_len)
                        span_id += 1
                    span_ids = self.__pad(span_ids, self.max_target_len)
                    new_source_ids.append(src_ids)
                    new_target_ids.append(tgt_ids)
                    new_pseudo_ids.append(pseudo_ids)
                    new_span_ids.append(span_ids)
                else:
                    new_source_ids.append(src_ids)
                    new_target_ids.append(tgt_ids)
                    new_pseudo_ids.append(pseudo_ids)
        if self.span_len > 1:
            return new_source_ids, new_target_ids, new_pseudo_ids, num_source_tokens, num_target_tokens, new_span_ids
        else:
            return new_source_ids, new_target_ids, new_pseudo_ids, num_source_tokens, num_target_tokens



