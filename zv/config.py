from pydantic import BaseModel


class BlogConfig(BaseModel):
    title: str
    description: str

    @classmethod
    def load(cls, d: dict):
        return BlogConfig(
            title=d["title"],
            description=d["description"],
        )


class ThemeConfig(BaseModel):
    name: str

    @classmethod
    def load(cls, d: dict):
        return ThemeConfig(
            name=d["name"],
        )


class PublicationConfig(BaseModel):
    path: str

    @classmethod
    def load(cls, d: dict):
        return PublicationConfig(
            path=d["path"],
        )


class Config(BaseModel):
    theme: ThemeConfig
    blog: BlogConfig
    publication: PublicationConfig

    @classmethod
    def load(cls, d: dict):
        print(d)
        return Config(
            theme=ThemeConfig.load(d["theme"]),
            blog=BlogConfig.load(d["blog"]),
            publication=PublicationConfig.load(d["publication"]),
        )
