from bitcoin_client.ledger_bitcoin import Client, AddressType, MultisigWallet, WalletPolicy
from bitcoin_client.ledger_bitcoin.exception.errors import IncorrectDataError


import pytest

# TODO: add tests with UI


def test_get_wallet_address_singlesig_legacy(client: Client):
    # legacy address (P2PKH)
    wallet = WalletPolicy(
        name="",
        descriptor_template="pkh(@0/**)",
        keys_info=[
            f"[350a4bc9/44'/1'/0']tpubDCwYjpDhUdPGP5rS3wgNg13mTrrjBuG8V9VpWbyptX6TRPbNoZVXsoVUSkCjmQ8jJycjuDKBb9eataSymXakTTaGifxR6kmVsfFehH1ZgJT",
        ],
    )
    assert client.get_wallet_address(wallet, None, 0,  0, False) == "qc8MCVJwQZTNdM2JhXhBs41fxZzZ8HN9cR"
    assert client.get_wallet_address(wallet, None, 1, 15, False) == "qbHdLA6nhsuNTvPoWZZm5RHSfXcLerpHLd"


def test_get_wallet_address_singlesig_wit(client: Client):
    # bech32 address (P2WPKH)
    wallet = WalletPolicy(
        name="",
        descriptor_template="wpkh(@0/**)",
        keys_info=[
            f"[350a4bc9/84'/1'/0']tpubDCtKfsNyRhULjZ9XMS4VKKtVcPdVDi8MKUbcSD9MJDyjRu1A2ND5MiipozyyspBT9bg8upEp7a8EAgFxNxXn1d7QkdbL52Ty5jiSLcxPt1P",
        ],
    )
    assert client.get_wallet_address(wallet, None, 0,  0, False) == "tq1qzdr7s2sr0dwmkwx033r4nujzk86u0cy6dcmgce"
    assert client.get_wallet_address(wallet, None, 1, 15, False) == "tq1qlrvzyx8jcjfj2xuy69du9trtxnsvjupefaqtd2"


def test_get_wallet_address_singlesig_sh_wit(client: Client):
    # wrapped segwit addresses (P2SH-P2WPKH)
    wallet = WalletPolicy(
        name="",
        descriptor_template="sh(wpkh(@0/**))",
        keys_info=[
            f"[350a4bc9/49'/1'/0']tpubDC871vGLAiKPcwAw22EjhKVLk5L98UGXBEcGR8gpcigLQVDDfgcYW24QBEyTHTSFEjgJgbaHU8CdRi9vmG4cPm1kPLmZhJEP17FMBdNheh3",
        ],
    )
    assert client.get_wallet_address(wallet, None, 0,  0, False) == "mNDsvaF9HHvEFaH6FmLRR3kAJoPBD3XfdW"
    assert client.get_wallet_address(wallet, None, 1, 15, False) == "mZXUNuos7tQiTr6JVTHcqbFfrSTf8zGzxx"


def test_get_wallet_address_singlesig_taproot(client: Client):
    # test for a native taproot wallet (bech32m addresses, per BIP-0086)

    wallet = WalletPolicy(
        name="",
        descriptor_template="tr(@0/**)",
        keys_info=[
            f"[350a4bc9/86'/1'/0']tpubDDKYE6BREvDsSWMazgHoyQWiJwYaDDYPbCFjYxN3HFXJP5fokeiK4hwK5tTLBNEDBwrDXn8cQ4v9b2xdW62Xr5yxoQdMu1v6c7UDXYVH27U",
        ],
    )

    res = client.get_wallet_address(wallet, None, 0, 0, False)
    assert res == "tq1pws8wvnj99ca6acf8kq7pjk7vyxknah0d9mexckh5s0vu2ccy68jsk4ulph"

    res = client.get_wallet_address(wallet, None, 0, 9, False)
    assert res == "tq1psl7eyk2jyjzq6evqvan854fts7a5j65rth25yqahkd2a765yvj0qmqh3ws"

    res = client.get_wallet_address(wallet, None, 1, 0, False)
    assert res == "tq1pmr60r5vfjmdkrwcu4a2z8h39mzs7a6wf2rfhuml6qgcp940x9cxsdrzysd"

    res = client.get_wallet_address(wallet, None, 1, 9, False)
    assert res == "tq1p98d6s9jkf0la8ras4nnm72zme5r03fexn29e3pgz4qksdy84ndpqm66nrr"


# Failure cases for default wallets

def test_get_wallet_address_default_fail_wrongkeys(client: Client):
    # 0 keys info should be rejected
    with pytest.raises(IncorrectDataError):
        client.get_wallet_address(WalletPolicy(
            name="",
            descriptor_template="pkh(@0/**)",
            keys_info=[],
        ), None, 0,  0, False)

    # more than 1 key should be rejected
    with pytest.raises(IncorrectDataError):
        client.get_wallet_address(WalletPolicy(
            name="",
            descriptor_template="pkh(@0/**)",
            keys_info=[
                f"[350a4bc9/44'/1'/0']tpubDCwYjpDhUdPGP5rS3wgNg13mTrrjBuG8V9VpWbyptX6TRPbNoZVXsoVUSkCjmQ8jJycjuDKBb9eataSymXakTTaGifxR6kmVsfFehH1ZgJT",
                f"[350a4bc9/44'/1'/0']tpubDCwYjpDhUdPGP5rS3wgNg13mTrrjBuG8V9VpWbyptX6TRPbNoZVXsoVUSkCjmQ8jJycjuDKBb9eataSymXakTTaGifxR6kmVsfFehH1ZgJT"
            ],
        ), None, 0,  0, False)

    # wrong BIP44 purpose should be rejected (here using 84' for a P2PKH address)
    with pytest.raises(IncorrectDataError):
        client.get_wallet_address(WalletPolicy(
            name="",
            descriptor_template="pkh(@0/**)",
            keys_info=[
                f"[350a4bc9/84'/1'/0']tpubDCtKfsNyRhULjZ9XMS4VKKtVcPdVDi8MKUbcSD9MJDyjRu1A2ND5MiipozyyspBT9bg8upEp7a8EAgFxNxXn1d7QkdbL52Ty5jiSLcxPt1P",
            ],
        ), None, 0,  0, False)

    # mismatching pubkey (claiming key origin "44'/1'/0'", but that's the extended pubkey for "84'/1'/0'"")
    with pytest.raises(IncorrectDataError):
        client.get_wallet_address(WalletPolicy(
            name="",
            descriptor_template="pkh(@0/**)",
            keys_info=[
                f"[350a4bc9/44'/1'/0']tpubDCtKfsNyRhULjZ9XMS4VKKtVcPdVDi8MKUbcSD9MJDyjRu1A2ND5MiipozyyspBT9bg8upEp7a8EAgFxNxXn1d7QkdbL52Ty5jiSLcxPt1P",
            ],
        ), None, 0,  0, False)

    # wrong master fingerprint
    with pytest.raises(IncorrectDataError):
        client.get_wallet_address(WalletPolicy(
            name="",
            descriptor_template="pkh(@0/**)",
            keys_info=[
                f"[42424242/44'/1'/0']tpubDCwYjpDhUdPGP5rS3wgNg13mTrrjBuG8V9VpWbyptX6TRPbNoZVXsoVUSkCjmQ8jJycjuDKBb9eataSymXakTTaGifxR6kmVsfFehH1ZgJT",
            ],
        ), None, 0,  0, False)

    # too large address_index, cannot be done non-silently
    with pytest.raises(IncorrectDataError):
        client.get_wallet_address(WalletPolicy(
            name="",
            descriptor_template="pkh(@0/**)",
            keys_info=[
                f"[350a4bc9/44'/1'/0']tpubDCwYjpDhUdPGP5rS3wgNg13mTrrjBuG8V9VpWbyptX6TRPbNoZVXsoVUSkCjmQ8jJycjuDKBb9eataSymXakTTaGifxR6kmVsfFehH1ZgJT",
            ],
        ), None, 0,  100000, False)


# Multisig


def test_get_wallet_address_multisig_legacy(client: Client):
    # test for a legacy p2sh multisig wallet

    wallet = MultisigWallet(
        name="Cold storage",
        address_type=AddressType.LEGACY,
        threshold=2,
        keys_info=[
            f"[5c9e228d/48'/1'/0'/0']tpubDEGquuorgFNb8bjh5kNZQMPtABJzoWwNm78FUmeoPkfRtoPF7JLrtoZeT3J3ybq1HmC3Rn1Q8wFQ8J5usanzups5rj7PJoQLNyvq8QbJruW",
            f"[350a4bc9/48'/1'/0'/0']tpubDFAqEGNyad35WQAZMmPD4vgBXnjH16RGciLdWekPe4f4d5JzoHVu1PS86Sy4Tm63vDf8rfV3UjifhrRuSUDfiZj5KPffTPyZ4ZXBKvjD8jm",
        ],
    )
    wallet_hmac = bytes.fromhex(
        "fa73e36119324fbe4cc1ca94aa842c6261526d44112a22164bc57c3335102b04"
    )

    res = client.get_wallet_address(wallet, wallet_hmac, 0, 0, False)
    assert res == "2Mx69MjHC4ViZAH1koVXPvVgaazbBCdr89j"


def test_get_wallet_address_multisig_sh_wit(client: Client):
    # test for a wrapped segwit multisig wallet

    wallet = MultisigWallet(
        name="Cold storage",
        address_type=AddressType.SH_WIT,
        threshold=2,
        keys_info=[
            f"[76223a6e/48'/1'/0'/1']tpubDE7NQymr4AFtcJXi9TaWZtrhAdy8QyKmT4U6b9qYByAxCzoyMJ8zw5d8xVLVpbTRAEqP8pVUxjLE2vDt1rSFjaiS8DSz1QcNZ8D1qxUMx1g",
            f"[350a4bc9/48'/1'/0'/1']tpubDFAqEGNyad35YgH8zxvxFZqNUoPtr5mDojs7wzbXQBHTZ4xHeVXG6w2HvsKvjBpaRpTmjYDjdPg5w2c6Wvu8QBkyMDrmBWdCyqkDM7reSsY",
        ],
    )
    wallet_hmac = bytes.fromhex(
        "1f498e7444841b883c4a63e2b88a5cad297c289d235794f8e3e17cf559ed0654"
    )

    res = client.get_wallet_address(wallet, wallet_hmac, 0, 0, False)
    assert res == "2MxAUTJh27foYtyp9dcSxP7RgaSwkkVCHTU"


def test_get_wallet_address_multisig_wit(client: Client):
    # test for a native segwit multisig wallet (bech32 address)

    wallet = MultisigWallet(
        name="Cold storage",
        address_type=AddressType.WIT,
        threshold=2,
        keys_info=[
            f"[76223a6e/48'/1'/0'/2']tpubDE7NQymr4AFtewpAsWtnreyq9ghkzQBXpCZjWLFVRAvnbf7vya2eMTvT2fPapNqL8SuVvLQdbUbMfWLVDCZKnsEBqp6UK93QEzL8Ck23AwF",
            f"[350a4bc9/48'/1'/0'/2']tpubDFAqEGNyad35aBCKUAXbQGDjdVhNueno5ZZVEn3sQbW5ci457gLR7HyTmHBg93oourBssgUxuWz1jX5uhc1qaqFo9VsybY1J5FuedLfm4dK",
        ],
    )
    wallet_hmac = bytes.fromhex(
        "d7c7a60b4ab4a14c1bf8901ba627d72140b2fb907f2b4e35d2e693bce9fbb371"
    )

    res = client.get_wallet_address(wallet, wallet_hmac, 0, 0, False)
    assert res == "tb1qmyauyzn08cduzdqweexgna2spwd0rndj55fsrkefry2cpuyt4cpsn2pg28"


def test_get_wallet_address_tr_script_pk(client: Client):
    wallet = WalletPolicy(
        name="Taproot foreign internal key, and our script key",
        descriptor_template="tr(@0/**,pk(@1/**))",
        keys_info=[
            "[76223a6e/48'/1'/0'/2']tpubDE7NQymr4AFtewpAsWtnreyq9ghkzQBXpCZjWLFVRAvnbf7vya2eMTvT2fPapNqL8SuVvLQdbUbMfWLVDCZKnsEBqp6UK93QEzL8Ck23AwF",
            "[350a4bc9/48'/1'/0'/2']tpubDFAqEGNyad35aBCKUAXbQGDjdVhNueno5ZZVEn3sQbW5ci457gLR7HyTmHBg93oourBssgUxuWz1jX5uhc1qaqFo9VsybY1J5FuedLfm4dK",
        ],
    )

    wallet_hmac = bytes.fromhex(
        "dae925660e20859ed8833025d46444483ce264fdb77e34569aabe9d590da8fb7"
    )

    res = client.get_wallet_address(wallet, wallet_hmac, 0, 0, False)
    assert res == "tb1pls9pp5cgcljpkjauxep03lv2c2yc2wcuua26p3ks6j2lq0vl9kjqf5rgm2"


def test_get_wallet_address_tr_script_sortedmulti(client: Client):
    wallet = WalletPolicy(
        name="Taproot single-key or multisig 2-of-2",
        descriptor_template="tr(@0/**,sortedmulti_a(2,@1/**,@2/**))",
        keys_info=[
            "[350a4bc9/48'/1'/0'/1']tpubDFAqEGNyad35YgH8zxvxFZqNUoPtr5mDojs7wzbXQBHTZ4xHeVXG6w2HvsKvjBpaRpTmjYDjdPg5w2c6Wvu8QBkyMDrmBWdCyqkDM7reSsY",
            "[76223a6e/48'/1'/0'/2']tpubDE7NQymr4AFtewpAsWtnreyq9ghkzQBXpCZjWLFVRAvnbf7vya2eMTvT2fPapNqL8SuVvLQdbUbMfWLVDCZKnsEBqp6UK93QEzL8Ck23AwF",
            "[350a4bc9/48'/1'/0'/2']tpubDFAqEGNyad35aBCKUAXbQGDjdVhNueno5ZZVEn3sQbW5ci457gLR7HyTmHBg93oourBssgUxuWz1jX5uhc1qaqFo9VsybY1J5FuedLfm4dK",
        ],
    )

    wallet_hmac = bytes.fromhex(
        "a3f31e9d7b70d1d967413488bae136a8b6c7afd1de0524deb6cf74f5c509b9ab"
    )

    res = client.get_wallet_address(wallet, wallet_hmac, 0, 0, False)
    assert res == "tb1pdzk72dnvz3246474p4m5a97u43h6ykt2qcjrrhk6y0fkg8hx2mvswwgvv7"


def test_get_wallet_address_large_addr_index(client: Client):
    # 2**31 - 1 is the largest index allowed, per BIP-32

    wallet = MultisigWallet(
        name="Cold storage",
        address_type=AddressType.WIT,
        threshold=2,
        keys_info=[
            "[76223a6e/48'/1'/0'/2']tpubDE7NQymr4AFtewpAsWtnreyq9ghkzQBXpCZjWLFVRAvnbf7vya2eMTvT2fPapNqL8SuVvLQdbUbMfWLVDCZKnsEBqp6UK93QEzL8Ck23AwF",
            "[350a4bc9/48'/1'/0'/2']tpubDFAqEGNyad35aBCKUAXbQGDjdVhNueno5ZZVEn3sQbW5ci457gLR7HyTmHBg93oourBssgUxuWz1jX5uhc1qaqFo9VsybY1J5FuedLfm4dK",
        ],
    )
    wallet_hmac = bytes.fromhex(
        "d7c7a60b4ab4a14c1bf8901ba627d72140b2fb907f2b4e35d2e693bce9fbb371"
    )

    client.get_wallet_address(wallet, wallet_hmac, 0, 2**31 - 1, False)

    # too large address_index, not allowed for an unhardened step
    with pytest.raises(IncorrectDataError):
        client.get_wallet_address(wallet, wallet_hmac, 0, 2**31, False)
