/**
 * Serverless Function: AI Vocabulary Explanation
 * 
 * This function proxies requests to Aliyun Qwen API
 * to avoid CORS issues when calling from browser.
 * 
 * Usage: POST /api/ai-explain
 * Body: { "word": "excavate" }
 */

export const config = {
    runtime: 'edge', // Use Edge runtime for faster response
};

export default async function handler(request) {
    // Handle CORS preflight requests
    if (request.method === 'OPTIONS') {
        return new Response(null, {
            status: 200,
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
        });
    }

    // Only allow POST requests
    if (request.method !== 'POST') {
        return new Response(
            JSON.stringify({ error: 'Method not allowed' }),
            {
                status: 405,
                headers: { 'Content-Type': 'application/json' },
            }
        );
    }

    try {
        // Parse request body
        const { word } = await request.json();

        if (!word || typeof word !== 'string') {
            return new Response(
                JSON.stringify({ error: 'Word is required' }),
                {
                    status: 400,
                    headers: { 'Content-Type': 'application/json' },
                }
            );
        }

        console.log(`Generating AI explanation for word: ${word}`);

        // Call Aliyun DashScope API
        const aliyunResponse = await fetch(
            'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
            {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${process.env.ALIYUN_API_KEY || 'sk-92b75e89aa404648b08741885f191e6b'}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model: 'qwen-plus',
                    input: {
                        messages: [
                            {
                                role: 'system',
                                content: 'You are an ESL English teacher. Explain vocabulary words with etymology, technical usage, related words, and examples. Provide bilingual (English + Traditional Chinese) explanations. Use HTML formatting with <br>, <strong>, <em> tags. Keep explanations concise but informative (max 300 words).',
                            },
                            {
                                role: 'user',
                                content: `Explain the word "${word}" in detail. Include: 1) Word Origin/Etymology, 2) Technical/Academic Usage, 3) Related Words (synonyms, word family), 4) Example sentence. Provide both English and Traditional Chinese (Cantonese-friendly) explanations. Format with HTML tags.`,
                            },
                        ],
                    },
                    parameters: {
                        temperature: 0.7,
                        max_tokens: 500,
                    },
                }),
            }
        );

        if (!aliyunResponse.ok) {
            const errorData = await aliyunResponse.json().catch(() => ({}));
            console.error('Aliyun API error:', aliyunResponse.status, errorData);
            
            return new Response(
                JSON.stringify({
                    error: `Aliyun API error: ${aliyunResponse.status}`,
                    details: errorData,
                }),
                {
                    status: aliyunResponse.status,
                    headers: { 'Content-Type': 'application/json' },
                }
            );
        }

        const data = await aliyunResponse.json();
        const aiExplanation = data.output?.text || 'No explanation generated';

        console.log('AI explanation generated successfully');

        // Return successful response with CORS headers
        return new Response(
            JSON.stringify({
                success: true,
                word: word,
                explanation: aiExplanation,
            }),
            {
                status: 200,
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                },
            }
        );

    } catch (error) {
        console.error('Serverless function error:', error);
        
        return new Response(
            JSON.stringify({
                error: 'Internal server error',
                message: error.message,
            }),
            {
                status: 500,
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            }
        );
    }
}
