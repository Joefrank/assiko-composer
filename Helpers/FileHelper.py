from pathlib import Path

class FileHelper: 
    BASE_DIR = Path(__file__).resolve().parent.parent

    @staticmethod
    def get_path(relative_path: str) -> Path:
        return FileHelper.BASE_DIR / relative_path
    
    @staticmethod 
    def get_asset_images_paths() -> str:        
        return  FileHelper.BASE_DIR / "Assets/Images"