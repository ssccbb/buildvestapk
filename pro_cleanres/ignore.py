# coding=utf-8

class IgnoreRule:

    @staticmethod
    def annotation(content):
        if content.startsWith("@") and content.endsWith(")"):
            return True
        return False
