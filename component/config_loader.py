import yaml
import os
import logging


def load_process_params_config() -> dict:
    """
    从 YAML 文件加载工艺参数配置。

    Returns:
        dict: 返回加载的配置字典。
    """
    # 获取当前脚本所在的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建相对路径
    file_path = os.path.join(script_dir, '../config/process_params_config.yaml')

    # 确保文件存在
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    else:
        logging.error(f"文件 {file_path} 不存在")
        return {}


def get_required_params(sub_process_type: str, config: dict) -> list:
    """
    获取指定子工艺类型所需的参数。

    Args:
        sub_process_type (str): 子工艺类型。
        config (dict): 从 YAML 文件加载的配置字典。

    Returns:
        list: 所需参数的列表。
    """
    process_types = config.get("sub_process_types", {})
    return process_types.get(sub_process_type, {}).get("required_params", [])
