#!/bin/bash

python train_quest.py \
--data_train data/qe/train/train.src.lc data/qe/train/train.mt.lc data/qe/train/train.align \
--data_train_y data/qe/train/train.tags \
--data_test data/qe/test/test.src.lc data/qe/test/test.mt.lc data/qe/test/test.align \
--data_test_y data/qe/test/test.tags \
--data_valid data/qe/dev/dev.src.lc data/qe/dev/dev.mt.lc data/qe/dev/dev.align \
--data_valid_y data/qe/dev/dev.tags \
--dictionaries data/qe/train/train.src.lc.json data/qe/train/train.mt.lc.json \
--embeddings data/qe/pretrain/ep_qe.en.vector.txt data/qe/pretrain/ep_qe.de.vector.txt
#--use_bilingual \
#--use_pretrain