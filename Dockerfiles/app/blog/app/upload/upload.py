import qiniu
from qiniu import BucketManager
from urlparse import urljoin


class QiNiuUpload(object):
    """docstring for QiNiuUpload"""

    def __init__(self, app):
        self.app = app
        self.QINIU_ACCESS_KEY = self.app.config['QINIU_ACCESS_KEY']
        self.QINIU_SECRET_KEY = self.app.config['QINIU_SECRET_KEY']
        self.PIC_BUCKET = self.app.config['PIC_BUCKET']
        self.PIC_DOMAIN = self.app.config['PIC_DOMAIN']

        self.auth = qiniu.Auth(self.QINIU_ACCESS_KEY, self.QINIU_SECRET_KEY)
        self.bucket_manager = BucketManager(self.auth)
        if not self.PIC_DOMAIN:
            self._base_url ='http://' + self.PIC_BUCKET + '.qiniudn.com'
        else:
            self._base_url = 'http://' + self.PIC_DOMAIN

    def get_token(self):
        return self.auth.upload_token(self.PIC_BUCKET)

    def get_bucket(self):
        self.bucket = BucketManager(self.auth)
        return self.bucket

    def save_data(self, filename, data):
        if not filename:
            filename = None
        if not data:
            return
        ret, info = qiniu.put_data(self.get_token(), filename, data)
        print ret
        print info
        if info.status_code == 200:
            return ret['key']
        else:
            return False

    def del_data(self, filename):
        if not filename:
            filename = None
        ret, info = self.get_bucket().delete(self.PIC_BUCKET, filename)
        print ret
        print info
        if info.status_code == 200:
            return True
        else:
            return False

    def list_data(self, prefix=None, limit=None):
        bucket = self.get_bucket()
        marker = None
        eof = False
        items = []
        while eof is False:
            ret, eof, info = bucket.list(
                self.PIC_BUCKET, prefix=prefix, marker=marker, limit=limit)
            marker = ret.get('marker', None)
            for item in ret['items']:
                print(item['key'])
                items.append(item['key'])
        if eof is not True:
            pass
        return items

    def get_data_info(self, filename):
        ret, info = self.get_bucket().stat(self.PIC_BUCKET, filename)
        print ret
        print info

    def get_data_url(self, filename):
        return urljoin(self._base_url, filename)
