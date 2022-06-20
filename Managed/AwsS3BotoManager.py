from Singleton import CSingleton

class CAwsS3BotoManager(CSingleton):
    __AccessKeyId = None
    __SecretKey = None
    __RegionName = None
    __BucketName = None
    __BucketUrl = None
    __count = None
    
    def loadConfig(self, config):
        self.__AccessKeyId = config["access_key_id"]
        self.__SecretKey = config["secret_key"]
        self.__RegionName = config["region_name"]
        self.__BucketName = config["bucket_name"]
        self.__BucketUrl = config["bucket_url"]
        self.__count = 0
        
    def getBucketUrl(self):
        return f"https://{self.__BucketUrl}"
    
    def uploadFile(self, path, filename, data):
        try:
            import boto3
            from uuid import uuid4
            
            arr = filename.split(".")
            ext = arr[-1]
            name = str(uuid4()).replace("-","")
            name += f"{self.__count}"
            name += ".%s" % ext
            
            self.__count = self.__count + 1
            
            s3_res = boto3.resource('s3', aws_access_key_id = self.__AccessKeyId, aws_secret_access_key = self.__SecretKey, region_name = self.__RegionName)
            s3_bucket = s3_res.Bucket(self.__BucketName)
            s3_bucket.put_object(Body=data, Key=f"{path}/{name}", ACL="public-read")
            return f"https://{self.__BucketUrl}/{path}/{name}"
        except Exception as e:
            print(e)
            return None
        