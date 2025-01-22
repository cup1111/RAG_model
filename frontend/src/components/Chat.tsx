import React, { useState, KeyboardEvent, ChangeEvent } from 'react';

// 定义消息接口
interface Message {
    content: string;  // 消息内容
    isUser: boolean;  // 是否是用户消息
}

// 聊天组件
export function Chat() {
    // 状态管理：消息历史和输入框
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isCodeMode, setIsCodeMode] = useState(false);  // 添加代码模式状态

    // 发送消息的异步函数
    const sendMessage = async () => {
        // 检查输入是否为空
        if (!input.trim()) return;

        // 创建用户消息对象
        const userMessage: Message = {
            content: input,
            isUser: true,
        };

        // 更新消息列表，添加用户消息
        setMessages(prev => [...prev, userMessage]);
        setInput('');  // 清空输入框

        try {
            // 发送请求到后端
            const response = await fetch('http://localhost:3000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: input,
                    isCodeMode: isCodeMode  // 添加模式标识
                }),
            });

            // 处理响应
            const data = await response.json();
            // 创建AI消息对象
            const aiMessage: Message = {
                content: data.response,
                isUser: false,
            };

            // 更新消息列表，添加AI回复
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('发送消息时出错:', error);
        }
    };

    // 修改输入处理函数
    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInput(e.target.value);
    };

    // 修改按键处理函数
    const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            void sendMessage();
        }
    };

    // 由于 sendMessage 是异步函数，添加 void 操作符
    const handleSendClick = () => {
        void sendMessage();
    };

    // 添加代码模式切换处理
    const handleCodeModeChange = (e: ChangeEvent<HTMLInputElement>) => {
        setIsCodeMode(e.target.checked);
    };

    // 渲染组件
    return (
        <div className="chat-container">
            <div className="mode-selector">
                <label>
                    <input
                        type="checkbox"
                        checked={isCodeMode}
                        onChange={handleCodeModeChange}
                    />
                    代码分析模式
                </label>
            </div>
            {/* 消息显示区域 */}
            <div className="messages">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`message ${message.isUser ? 'user' : 'ai'}`}
                    >
                        {message.content}
                    </div>
                ))}
            </div>
            {/* 输入区域 */}
            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    placeholder={isCodeMode ? "请输入要分析的代码..." : "输入消息..."}
                />
                <button onClick={handleSendClick}>发送</button>
            </div>
        </div>
    );
} 