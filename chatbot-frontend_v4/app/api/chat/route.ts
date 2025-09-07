import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { pergunta } = body

    if (!pergunta) {
      return NextResponse.json({ error: "Pergunta é obrigatória" }, { status: 400 })
    }

    // Substitua pela URL do seu backend real
    const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000"

    const response = await fetch(`${BACKEND_URL}/responder`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ pergunta }),
    })

    if (!response.ok) {
      throw new Error(`Backend retornou status ${response.status}`)
    }

    const responseText = await response.text()

    // Se a resposta for JSON, extrair apenas o valor da string
    try {
      const jsonResponse = JSON.parse(responseText)
      // Se for um objeto com uma propriedade string, retornar apenas o valor
      if (typeof jsonResponse === "object" && jsonResponse !== null) {
        const firstValue = Object.values(jsonResponse)[0]
        if (typeof firstValue === "string") {
          return new NextResponse(firstValue, {
            headers: { "Content-Type": "text/plain" },
          })
        }
      }
      // Se for uma string direta no JSON, retornar ela
      if (typeof jsonResponse === "string") {
        return new NextResponse(jsonResponse, {
          headers: { "Content-Type": "text/plain" },
        })
      }
    } catch {
      // Se não for JSON válido, tratar como texto simples
    }

    // Retornar como texto simples
    return new NextResponse(responseText, {
      headers: { "Content-Type": "text/plain" },
    })
  } catch (error) {
    console.error("Erro na API:", error)
    return NextResponse.json({ error: "Erro interno do servidor" }, { status: 500 })
  }
}
