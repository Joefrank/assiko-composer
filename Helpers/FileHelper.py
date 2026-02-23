from pathlib import Path

class FileHelper: 
    BASE_DIR = Path(__file__).resolve().parent.parent

    @staticmethod 
    def get_asset_paths() -> str:        
        return  FileHelper.BASE_DIR / "Assets/Images"