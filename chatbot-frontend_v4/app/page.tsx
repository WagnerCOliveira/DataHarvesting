"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Send, Bot, User } from "lucide-react"

interface Message {
  id: string
  text: string
  isUser: boolean
  timestamp: Date
}

export default function ChatbotPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      isUser: true,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputValue("")
    setIsLoading(true)

    try {
      // Substitua pela URL do seu backend
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ pergunta: inputValue }),
      })

      if (!response.ok) {
        throw new Error("Erro na comunicação com o servidor")
      }

      const data = await response.text()

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data,
        isUser: false,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente.",
        isUser: false,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      inputRef.current?.focus()
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex flex-col h-screen bg-background">
      {/* Header */}
      <div className="border-b border-border p-4">
        <div className="flex items-center gap-2">
          <Bot className="h-6 w-6 text-primary" />
          <h1 className="text-xl font-semibold">Chatbot Assistant</h1>
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground mt-8">
            <Bot className="h-12 w-12 mx-auto mb-4 text-muted-foreground/50" />
            <p>Olá! Como posso ajudá-lo hoje?</p>
            <p className="text-sm mt-2">Digite sua pergunta abaixo para começar.</p>
            <p className="text-sm mt-2">É um trabalho de web scraping no website https://quotes.toscrape.com/ e que 
              gerou dados sobres authores renomados e suas citações. </p>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className={`flex gap-3 ${message.isUser ? "justify-end" : "justify-start"}`}>
            {!message.isUser && (
              <div className="flex-shrink-0">
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                  <Bot className="h-4 w-4 text-primary" />
                </div>
              </div>
            )}

            <Card className={`max-w-[80%] p-3 ${message.isUser ? "bg-primary text-primary-foreground" : "bg-card"}`}>
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
              <p
                className={`text-xs mt-2 opacity-70 ${
                  message.isUser ? "text-primary-foreground/70" : "text-muted-foreground"
                }`}
              >
                {message.timestamp.toLocaleTimeString()}
              </p>
            </Card>

            {message.isUser && (
              <div className="flex-shrink-0">
                <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
                  <User className="h-4 w-4 text-secondary-foreground" />
                </div>
              </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
                <Bot className="h-4 w-4 text-primary" />
              </div>
            </div>
            <Card className="bg-card p-3">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce"></div>
                </div>
                <span className="text-sm text-muted-foreground">Digitando...</span>
              </div>
            </Card>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - Fixed at bottom */}
      <div className="border-t border-border p-4 bg-background">
        <div className="flex gap-2 max-w-4xl mx-auto">
          <Input
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Digite sua pergunta..."
            disabled={isLoading}
            className="flex-1"
            autoFocus
          />
          <Button onClick={sendMessage} disabled={!inputValue.trim() || isLoading} size="icon">
            <Send className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  )
}
