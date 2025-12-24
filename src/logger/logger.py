import json
import logging
import logging.config
from pathlib import Path

# from ..utils import read_json


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def setup_logging(sva_dir, log_config="src/logger/logger_config.json", default_level=logging.INFO, log_filename=None):
    """配置logger

    Args:
        sva_dir (_type_): _description_
        log_config (str, optional): _description_. Defaults to 'logger/logger_config.json'.
        default_level (_type_, optional): _description_. Defaults to logging.INFO.
        log_filename (str, optional): 日志文件名（如 "info.log", "info2.log"），如果提供则使用此文件名，
                                      否则使用配置文件中的默认文件名
    """
    log_config_path = Path(log_config)
    sva_dir = Path(sva_dir)
    if log_config_path.is_file():
        config = read_json(log_config_path)
        # 修改日志路径,相对路径改绝对路径
        for _, handler in config["handlers"].items():
            if "filename" in handler:
                # 如果指定了 log_filename，则使用指定的文件名，否则使用配置文件中的文件名
                if log_filename:
                    handler["filename"] = str(sva_dir / log_filename)
                else:
                    handler["filename"] = str(sva_dir / handler["filename"])
        logging.config.dictConfig(config)
    else:
        print("Warning: logging configuration file is not found in {}.".format(log_config))
        logging.basicConfig(level=default_level)


if __name__ == "__main__":
    # 添加utils路径
    # 测试logger配置
    setup_logging(Path("/home/wangtuo/workspace/research/PYG/Template/testdir"))
    logger = logging.getLogger(__name__)
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")
