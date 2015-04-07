from storages.backends import s3boto

class FixAdminStorage(s3boto.S3BotoStorage):
    """Unfortunately necessary to fix admin S3 paths."""
    def url(self, name):
        url = super(FixAdminStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url
