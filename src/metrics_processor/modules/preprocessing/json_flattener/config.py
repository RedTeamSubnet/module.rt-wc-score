"""Configuration for JSON data flattening."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ExtraBaseModel(BaseModel):
    """Base model with extra configuration."""

    class Config:
        extra = "allow"


class MouseMovement(BaseModel):
    x: int
    y: int
    timestamp: str


class MouseMetrics(BaseModel):
    movements: List[MouseMovement] = []
    clicks: List[dict] = []
    mouseDowns: List[dict] = []
    mouseUps: List[dict] = []


class KeyboardMetrics(BaseModel):
    keypresses: List[dict] = []
    keydowns: List[dict] = []
    keyups: List[dict] = []
    specificKeyEvents: List[dict] = []


class SignInButtonMetrics(BaseModel):
    hoverToClickTime: Optional[float] = None
    mouseLeaveCount: int = 0


class Metrics(BaseModel):
    mouse: MouseMetrics = Field(default_factory=MouseMetrics)
    keyboard: KeyboardMetrics = Field(default_factory=KeyboardMetrics)
    signInButton: SignInButtonMetrics = Field(default_factory=SignInButtonMetrics)


class InputData(BaseModel):
    project_id: Optional[str] = None
    user_id: Optional[str] = None
    metrics: Metrics = Field(default_factory=Metrics)

    class Config:
        extra = "allow"


_FIELD_MAPPING = {
    "project_id": ["project_id"],
    "user_id": ["user_id"],
    "mouse_movements": ["metrics", "mouse", "movements"],
    "mouse_clicks": ["metrics", "mouse", "clicks"],
    "mouse_mouseDowns": ["metrics", "mouse", "mouseDowns"],
    "mouse_mouseUps": ["metrics", "mouse", "mouseUps"],
    "keyboard_keypresses": ["metrics", "keyboard", "keypresses"],
    "keyboard_keydowns": ["metrics", "keyboard", "keydowns"],
    "keyboard_keyups": ["metrics", "keyboard", "keyups"],
    "keyboard_specificKeyEvents": ["metrics", "keyboard", "specificKeyEvents"],
    "signInButton_hoverToClickTime": ["metrics", "signInButton", "hoverToClickTime"],
    "signInButton_mouseLeaveCount": ["metrics", "signInButton", "mouseLeaveCount"],
}


class JsonDataFlattenerConfigPM(ExtraBaseModel):
    field_mapping: Dict[str, List[str]] = Field(default_factory=lambda: _FIELD_MAPPING)
    input_data: InputData = Field(default_factory=InputData)
    is_validate: bool = Field(default=True)
