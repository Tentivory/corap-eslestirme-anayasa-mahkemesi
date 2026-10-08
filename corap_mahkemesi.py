#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corap Eslestirme Anayasa Mahkemesi.

Tek kalan corabin anayasal statüsünü tespit eder.
Baglayici degildir. Ayaklar serbesttir.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import textwrap
from dataclasses import asdict, dataclass


HEYET = (
    "Baskan Corap (topugu saglam)",
    "Uye Terlik (gorevli, ayakkabi degil)",
    "Raportor Tüy (dosyaya karismis, cikarilamiyor)",
)

KARSI_OYLAR = (
    "Bu corap esini kaybetmedi, esinden bosandi. Bosanma protokolu yok.",
    "Siyah ile lacivert arasindaki fark, gozluk takmayan heyet icin siyasi degil optiktir.",
    "Makine corabi yutmamistir. Makine sadece sessiz ortaktir.",
    "Tek corap giymek ifade ozgurlugudur. Koku da ifadedir. Sinirli yorum.",
    "Emsal karar yoktur cunku emsal corap da kayiptir.",
)

HUKUMLER = (
    "ESLESTIRILDI",
    "IADESI ISTENDI",
    "YETKISIZLIK",
    "TEK BASINA YASAMA ORGANI SAYILDI",
    "MAKUL SUPHE ILE CEKMECEDE TUTUKLU",
)


@dataclass
class Karar:
    esas_no: str
    corap: str
    hukum: str
    gerekce: str
    karsi_oy: str
    heyet: tuple


def esas_no(corap: str) -> str:
    ozet = hashlib.sha256(corap.encode("utf-8")).hexdigest()[:6].upper()
    return f"2026/{int(ozet, 16) % 9000 + 1000}-E"


def gerekce_yaz(corap: str, hukum: str) -> str:
    parca = textwrap.fill(
        f"Basvurucu corap '{corap}' cekmeceden tek basina cikmistir. "
        f"Heyet, esin yoklugunu yokluk olarak degil, usuli eksiklik olarak gormustur. "
        f"Bu nedenle hukum: {hukum}. Infaz, kullanicinin ayagina birakilmistir. "
        f"Karar, corabin rengine bakilmaksizin, delik sayisi birden fazlaysa agirlastirici sebep sayilir.",
        width=78,
    )
    return parca


def yargila(corap: str, tohum: int | None = None) -> Karar:
    rnd = random.Random(tohum if tohum is not None else corap)
    hukum = rnd.choice(HUKUMLER)
    return Karar(
        esas_no=esas_no(corap),
        corap=corap.strip() or "kimligi belirsiz gri corap",
        hukum=hukum,
        gerekce=gerekce_yaz(corap, hukum),
        karsi_oy=rnd.choice(KARSI_OYLAR),
        heyet=HEYET,
    )


def yazdir(karar: Karar) -> None:
    cizgi = "=" * 62
    print(cizgi)
    print(" CORAP ESLESTIRME ANAYASA MAHKEMESI")
    print(" Baglayici olmayan gerekceli karar")
    print(cizgi)
    print(f"Esas no : {karar.esas_no}")
    print(f"Corap   : {karar.corap}")
    print(f"Heyet   : {', '.join(karar.heyet)}")
    print("-" * 62)
    print(karar.gerekce)
    print("-" * 62)
    print(f"HUKUM   : {karar.hukum}")
    print(f"Karsi oy: {karar.karsi_oy}")
    print(cizgi)
    print("Damga: 08 Ekim 2026 | Kayyum Grok | Tentivory")
    print("Muhur: ciddi degil, ciddiye alinmistir.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Tek corabi yargilar. Sonuc ayakkabi icinde test edilmelidir."
    )
    parser.add_argument(
        "--dava",
        default="sol ayak, lacivert, topukta supheli incelme",
        help="Yargilanacak corabin tarifi",
    )
    parser.add_argument("--json", action="store_true", help="Karari JSON yaz")
    parser.add_argument("--tohum", type=int, default=None, help="Tekrar edilebilir durusma")
    args = parser.parse_args(argv)

    karar = yargila(args.dava, args.tohum)
    if args.json:
        veri = asdict(karar)
        veri["heyet"] = list(karar.heyet)
        print(json.dumps(veri, ensure_ascii=False, indent=2))
    else:
        yazdir(karar)
    return 0


if __name__ == "__main__":
    sys.exit(main())
