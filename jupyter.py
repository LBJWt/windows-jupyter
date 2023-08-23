import os
import subprocess
import traceback
import socket
from utils.logutils import log

python_path = "python"
scripts_path = "python\Scripts"


def is_installed(model):
    try:
        # 尝试运行 python 命令
        result = subprocess.run([model, "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 检查返回结果
        if result.returncode == 0:
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def install_pip_module():
    if not is_installed("pip"):
        # 安装 pip 模块
        try:
            new_path = os.path.join(os.getcwd(), f'python')
            subprocess.check_call(["python", f'{new_path}\get-pip.py'])
            log.info("成功安装 pip 模块")
        except subprocess.CalledProcessError:
            log.info("安装 pip 模块时出错")


def configure_path(path):
    # Assuming the path to add is '/path/to/python/bin'
    new_path = os.path.join(os.getcwd(), f'{path}')
    # 获取当前的PATH环境变量
    current_path = os.environ["PATH"]
    # 在当前的PATH后追加新路径，并使用os.pathsep分隔
    new_path_value = current_path + os.pathsep + new_path
    # 更新环境变量
    os.environ["PATH"] = new_path_value


def configure_path_env_variable():
    if not is_installed("pip") and is_installed("python"):
        env_var_name = "PATH"
        python_path = os.path.join(os.getcwd(), f'python')
        scripts_path = os.path.join(os.getcwd(), f'python\Scripts')
        env_var_value = python_path + os.pathsep + scripts_path
        try:
            # 设置环境变量
            configure_path(f'python')
            configure_path(f'python\Scripts')
            subprocess.check_call(["setx", env_var_name, f"%{env_var_name}%;{env_var_value}"])
            log.info(f"成功追加环境变量: {env_var_name}={env_var_value}")
        except subprocess.CalledProcessError:
            log.info(f"追加环境变量时出错: {env_var_name}")


def change_mirror_source():
    if not is_installed("pip"):
        # 更换镜像源pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
        mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
        os.system('pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple')
        log.info(f"已更换镜像源：{mirror_url}")


def install_jupyter():
    if not is_installed("jupyter"):
        # 使用 pip 安装 jupyter
        try:
            subprocess.check_call(["python", "-m", "pip", "install", "jupyter_kernel_gateway"])
            log.info("成功安装 Jupyter")
        except subprocess.CalledProcessError:
            log.info("安装 Jupyter 时出错")


def start_jupyter():
    # 启动 Jupyter  start /B jupyter kernelgateway
    cmd = ['jupyter', 'kernelgateway', '--KernelGatewayApp.ip=0.0.0.0', '--KernelGatewayApp.port=18012',
           '--KernelGatewayApp.allow_credentials=*', '--KernelGatewayApp.allow_headers=*',
           '--KernelGatewayApp.allow_methods=*', '--KernelGatewayApp.allow_origin=*']
    try:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True)
        log.info("Jupyter kernel gateway 启动成功")
    except OSError as error:
        log.error(error)


def is_running():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        result = s.connect_ex(('127.0.0.1', 18012))
        s.close()
        if result == 0:
            log.info("AI-Link.exe is already running or port conflict!")
            return True
        else:
            return False
    except:
        log.info("Exception of is_running:{0}".format(traceback.format_exc()))
        return False


def main_process():
    if not is_running():
        # 配置环境变量
        configure_path_env_variable()
        # 安装pip模块
        install_pip_module()
        # 更换镜像源
        change_mirror_source()
        # 使用pip进行安装jupyter
        install_jupyter()
        # 启动jupyter
        start_jupyter()


if __name__ == "__main__":
    main_process()
