const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export interface ParsedItem {
  name: string;
  quantity: number;
}

export interface Seller {
  company: string;
  link: string;
}

export interface ItemWithSellers extends ParsedItem {
  sellers: Seller[];
}

export const apiClient = {
  /**
   * Health check endpoint
   */
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  },

  /**
   * Parse BOM file and extract part names and quantities
   */
  async parseBOM(file: File): Promise<ParsedItem[]> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/parse-bom`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to parse BOM');
    }

    const result = await response.json();
    return result.data;
  },

  /**
   * Get seller information for parsed items
   */
  async getSellers(items: ParsedItem[], apiKey?: string): Promise<ItemWithSellers[]> {
    const response = await fetch(`${API_BASE_URL}/api/get-sellers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        items,
        api_key: apiKey,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to get seller information');
    }

    const result = await response.json();
    return result.data;
  },

  /**
   * Complete pipeline: parse BOM and get seller info
   */
  async processBOM(file: File): Promise<{ parsed_data: ParsedItem[]; seller_info: ItemWithSellers[] }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/api/process-bom`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to process BOM');
    }

    const result = await response.json();
    return {
      parsed_data: result.parsed_data,
      seller_info: result.seller_info,
    };
  },
};
