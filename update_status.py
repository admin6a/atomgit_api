#!/usr/bin/env python3
"""
自动点击AtomGit页面"免费领取"按钮的脚本
通过GitHub Actions定时执行，实现自动领取功能
每日凌晨4:00固定执行 (UTC+8)
"""

import os
import time
import random
from datetime import datetime
import logging
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 配置UTC+8时区
UTC8 = pytz.timezone('Asia/Shanghai')

# 配置日志
class UTC8Formatter(logging.Formatter):
    """自定义日志格式化器，使用UTC+8时区"""
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=UTC8)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

# 配置日志处理器
handler = logging.StreamHandler()
handler.setFormatter(UTC8Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# 配置根日志记录器
logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
)
logger = logging.getLogger(__name__)

class AntiDetectionMechanism:
    """反检测机制实现"""

    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

    def get_random_user_agent(self):
        """获取随机User-Agent"""
        return random.choice(self.user_agents)

    def random_delay(self, min_seconds=2, max_seconds=10):
        """随机延迟"""
        delay = random.uniform(min_seconds, max_seconds)
        logger.info(f"随机延迟 {delay:.2f} 秒")
        time.sleep(delay)

    def human_like_delay(self):
        """模拟人类操作的延迟"""
        short_delay = random.uniform(0.5, 2.0)
        time.sleep(short_delay)

class AtomGitButtonClicker:
    """AtomGit页面按钮点击器"""

    def __init__(self):
        """初始化反检测机制"""
        self.anti_detection = AntiDetectionMechanism()

    def click_free_claim_button(self):
        """自动点击AtomGit页面的"免费领取"按钮"""
        cookie = os.getenv('ATOMGIT_COOKIE')
        if not cookie:
            raise ValueError("ATOMGIT_COOKIE环境变量未设置")

        logger.info("开始自动点击AtomGit页面的'免费领取'按钮...")

        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f'--user-agent={self.anti_detection.get_random_user_agent()}')

        driver = None
        try:
            # 初始化WebDriver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # 访问AtomGit页面
            url = "https://ai.atomgit.com/serverless-api"
            logger.info(f"访问页面: {url}")
            driver.get(url)

            # 设置cookie
            logger.info("设置Cookie...")
            for cookie_item in cookie.split('; '):
                if '=' in cookie_item:
                    name, value = cookie_item.split('=', 1)
                    driver.add_cookie({
                        'name': name.strip(),
                        'value': value.strip(),
                        'domain': 'ai.atomgit.com'
                    })

            # 刷新页面使cookie生效
            logger.info("刷新页面使Cookie生效...")
            driver.refresh()

            # 等待页面加载
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # 增加等待时间，确保页面完全加载
            logger.info("等待页面完全加载...")
            time.sleep(10)

            self.anti_detection.human_like_delay()

            # 查找并点击"免费领取"按钮
            try:
                # 尝试通过多种方式定位按钮
                button = None

                # 尝试通过文本内容定位
                try:
                    button = driver.find_element(By.XPATH, "//button[contains(text(), '免费领取')]")
                    logger.info("通过文本内容找到'免费领取'按钮")
                except Exception:
                    pass

                # 尝试通过CSS选择器定位（如果前面的方法失败）
                if not button:
                    try:
                        button = driver.find_element(By.CSS_SELECTOR, "button:contains('免费领取')")
                        logger.info("通过CSS选择器找到'免费领取'按钮")
                    except Exception:
                        pass

                # 尝试通过其他常见按钮类名定位
                if not button:
                    try:
                        buttons = driver.find_elements(By.TAG_NAME, "button")
                        for btn in buttons:
                            if "免费领取" in btn.text:
                                button = btn
                                logger.info("通过遍历按钮找到'免费领取'按钮")
                                break
                    except Exception:
                        pass

                if button:
                    # 等待按钮可点击
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(button)
                    )

                    # 点击按钮
                    button.click()
                    logger.info("'免费领取'按钮点击成功")

                    # 等待操作完成
                    logger.info("等待操作完成...")
                    time.sleep(8)  # 增加等待时间确保操作完成

                    return True
                else:
                    logger.error("未找到'免费领取'按钮")
                    return False

            except Exception as e:
                logger.error(f"点击按钮时出错: {e}")
                return False

        except Exception as e:
            logger.error(f"浏览器操作失败: {e}")
            return False
        finally:
            if driver:
                driver.quit()

    def run_auto_click(self):
        """执行自动点击流程"""
        logger.info("开始执行自动点击流程...")

        try:
            # 执行点击操作
            success = self.click_free_claim_button()

            if success:
                logger.info("自动点击操作成功")
                logger.info("下次执行：每日凌晨4:00 (UTC+8)")
                return True
            else:
                logger.error("自动点击操作失败")
                return False

        except Exception as e:
            logger.error(f"自动点击流程执行失败: {e}")
            return False

def main():
    """主函数"""
    try:
        button_clicker = AtomGitButtonClicker()
        success = button_clicker.run_auto_click()

        if success:
            logger.info("自动点击流程执行成功")
            exit(0)
        else:
            logger.error("自动点击流程执行失败")
            exit(1)

    except Exception as e:
        logger.error(f"程序执行异常: {e}")
        exit(1)

if __name__ == "__main__":
    main()