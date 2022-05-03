import OpenSSL
import jks

keystore = jks.KeyStore.load('/home/gabriel/.keystore', '1gabi2')

print(keystore.private_keys)
print(keystore.certs)
print(keystore.secret_keys)

ASN1 = OpenSSL.crypto.FILETYPE_ASN1


def jksfile2context(jks_file, passphrase, key_alias, key_password=None):
    keystore = jks.KeyStore.load(jks_file, passphrase)
    pk_entry = keystore.private_keys[key_alias]

    # if the key could not be decrypted using the store password,
    # decrypt with a custom password now
    if not pk_entry.is_decrypted():
        pk_entry.decrypt(key_password)

    pkey = OpenSSL.crypto.load_privatekey(ASN1, pk_entry.pkey)
    public_cert = OpenSSL.crypto.load_certificate(ASN1,
                                                  pk_entry.cert_chain[0][1])
    trusted_certs = [OpenSSL.crypto.load_certificate(ASN1, cert.cert)
                     for alias, cert in keystore.certs]

    ctx = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_METHOD)
    ctx.use_privatekey(pkey)
    ctx.use_certificate(public_cert)
    ctx.check_privatekey()  # want to know ASAP if there is a problem
    cert_store = ctx.get_cert_store()
    for cert in trusted_certs:
        cert_store.add_cert(cert)

    return ctx
