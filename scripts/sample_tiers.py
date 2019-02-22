#!/usr/bin/env python

"""
A utility script that will populate the database
with sample payment tiers.

Usage:
    python scripts/sample_tiers.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reviews.core.models import database
from reviews.home.models import Tier


tiers = {
    'Gold': {
        'sku': 'sku_CI25CoewzpG1rg',
        'price': 19.99,
        'details': '30 Reviews',
        'description': 'Step into the spotlight and get the critical insights '
                       'you need to take your music to the next level! Get a '
                       'Track Rating to see how your song connects with a '
                       'diverse group of music fans!',
    },
    'Platinum': {
        'sku': 'sku_CI25JMdlgYZ4nh',
        'price': 49.99,
        'details': '75 Reviews',
        'description': 'Includes Gold Rating services, plus discover where '
                       'your song ranks among a diverse crowd of reviewers. '
                       'If you achieve a high Track Rating, you can unlock '
                       'TuneGO radio and sync licensing opportunities to '
                       'have your music featured in TV, movies, video games '
                       'and more!',
    },
    'Diamond': {
        'sku': 'sku_CI25WE3Natp2b7',
        'price': 99.99,
        'details': '200 Reviews',
        'description': 'Includes Gold and Platinum Rating services, plus '
                       'compare your song to 100,000 major label releases '
                       'in your genre to gain insight on your music’s market '
                       'potential and likelihood of chart success! If you '
                       'achieve a high Track Rating, you can qualify to '
                       'connect with legendary producers, A&R executives '
                       'and even music labels!',
    },
}


def main():
    with database:
        for tier_type, tier_info in tiers.items():
            print(Tier.create(
                sku=tier_info['sku'],
                type=tier_type,
                price=tier_info['price'],
                details=tier_info['details'],
                description=tier_info['description'],
            ))


if __name__ == '__main__':
    main()
