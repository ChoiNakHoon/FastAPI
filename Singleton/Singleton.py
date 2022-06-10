
# 싱글톤 디자인 패턴은 글로벌하게 접근 가능한 하나의 객체를 제공하는 패턴

class CSingleton:
    
    # instance 초기화
    __instance = None
    
    # class method
    # class 매소드는 static매소드와 동일한 방식으로 @classmethod를 명시해줘야 합니다. class매소드 또한 static매소드와 마찬가지로 클래스를 인스턴스화 하지 않아도 호출이 가능

    @classmethod
    def __getInstance(cls):
        return cls.__instance
    
    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance