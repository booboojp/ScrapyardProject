from screenshot import ScreenshotManager, PathType
def main():
    manager = ScreenshotManager()
    
    manager.save("test_save.png")
    
    abs_path = manager.save_and_get_path("test_path_abs.png")
    print(f"Absolute path: {abs_path}")
    
    local_path = manager.save_and_get_path("test_path_local.png", path_type=PathType.LOCAL)
    print(f"Local path: {local_path}")
    
    abs_path = manager.process("test_process_abs.png", return_path=True)
    print(f"Process returned absolute path: {abs_path}")
    
    local_path = manager.process("test_process_local.png", return_path=True, path_type=PathType.LOCAL)
    print(f"Process returned local path: {local_path}")

if __name__ == "__main__":
    main()