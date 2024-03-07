import os
from functools import cached_property

from docx import Document
from utils import Log

log = Log('BookDir')


class BookDir:
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    def __str__(self):
        return f"BookDir({self.dir_path})"

    def get_doc_stats(self, doc_path: str):
        doc = Document(doc_path)
        n_para = 0
        n_words = 0
        n_chars = 0
        for para in doc.paragraphs:
            n_para += 1
            n_words += len(para.text.split())
            n_chars += len(para.text)
        return dict(n_para=n_para, n_words=n_words, n_chars=n_chars)

    @cached_property
    def stats_idx(self):
        log.debug(f'Analyzing {self}...')
        stats_idx = {}
        i_doc = 0
        for file_name in os.listdir(self.dir_path):
            if not file_name.endswith('.docx'):
                break
            stats = self.get_doc_stats(os.path.join(self.dir_path, file_name))
            stats_idx[file_name] = stats
            n_words = stats['n_words']
            file_name_only = file_name.split('.')[0]
            i_doc += 1
            log.debug(f'{i_doc:02}) {file_name_only:<20} {n_words:>10,}')

        return stats_idx

    @cached_property
    def aggregate_stats(self):
        log.debug(f'Analyzing {self}...')
        aggregate_stats = dict(n_para=0, n_words=0, n_chars=0)
        for stats in self.stats_idx.values():
            aggregate_stats['n_para'] += stats['n_para']
            aggregate_stats['n_words'] += stats['n_words']
            aggregate_stats['n_chars'] += stats['n_chars']

        n_words = aggregate_stats['n_words']
        log.info(f'n_words={n_words:,}')
        return aggregate_stats

    def analyze(self):
        self.aggregate_stats
        os.startfile(self.dir_path)
