import React, { useState, KeyboardEvent, ChangeEvent } from 'react';
import ReactMarkdown from 'react-markdown';

// Message interface definition
interface Message {
    content: string;  // Message content
    isUser: boolean;  // Whether it's a user message
}

// Chat component
export function Chat() {
    // State management: message history and input
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isCodeMode, setIsCodeMode] = useState(false);  // Add code mode state

    // Async function to send message
    const sendMessage = async () => {
        // Check if input is empty
        if (!input.trim()) return;

        // Create user message object
        const userMessage: Message = {
            content: input,
            isUser: true,
        };

        // Update message list with user message
        setMessages(prev => [...prev, userMessage]);
        setInput('');  // Clear input

        try {
            // Send request to backend
            const response = await fetch('http://localhost:3000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: input,
                    isCodeMode: isCodeMode  // Add mode identifier
                }),
            });

            // Handle response
            const data = await response.json();
            // Create AI message object
            const aiMessage: Message = {
                content: data.response,
                isUser: false,
            };

            // Update message list with AI response
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    // Input change handler
    const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
        setInput(e.target.value);
    };

    // Key press handler
    const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            void sendMessage();
        }
    };

    // Since sendMessage is async, add void operator
    const handleSendClick = () => {
        void sendMessage();
    };

    // Add code mode toggle handler
    const handleCodeModeChange = (e: ChangeEvent<HTMLInputElement>) => {
        setIsCodeMode(e.target.checked);
    };

    // Render component
    return (
        <div className="chat-container">
            <div className="mode-selector">
                <label>
                    <input
                        type="checkbox"
                        checked={isCodeMode}
                        onChange={handleCodeModeChange}
                    />
                    Code Analysis Mode
                </label>
            </div>
            {/* Message display area */}
            <div className="messages">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`message ${message.isUser ? 'user' : 'ai'}`}
                    >
                        {message.isUser ? (
                            <span>{message.content}</span>
                        ) : (
                            <ReactMarkdown>{message.content}</ReactMarkdown>
                        )}
                    </div>
                ))}
            </div>
            {/* Input area */}
            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    placeholder={isCodeMode ? "Enter code to analyze..." : "Enter message..."}
                />
                <button onClick={handleSendClick}>Send</button>
            </div>
        </div>
    );
} 