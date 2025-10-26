import { useState } from "react";
import FileUpload from "@/components/FileUpload";
import BOMPreview from "@/components/BOMPreview";
import SellerResults from "@/components/SellerResults";
import { Package, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { apiClient, ItemWithSellers } from "@/lib/api";
import * as XLSX from "xlsx";

const Index = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [bomData, setBomData] = useState<string[][]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [sellerResults, setSellerResults] = useState<ItemWithSellers[]>([]);
  const { toast } = useToast();

  const handleFileSelect = async (file: File) => {
    setSelectedFile(file);

    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    let data: string[][] = [];

    if (fileExtension === '.csv' || fileExtension === '.txt') {
      // Parse CSV/TXT file
      const text = await file.text();
      const lines = text.split('\n').filter(line => line.trim());
      data = lines.map(line => {
        // Simple CSV parsing (handles basic cases)
        return line.split(',').map(cell => cell.trim().replace(/^"|"$/g, ''));
      });
    } else if (fileExtension === '.xlsx' || fileExtension === '.xls') {
      // Parse Excel file
      const arrayBuffer = await file.arrayBuffer();
      const workbook = XLSX.read(arrayBuffer, { type: 'array' });
      const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
      const jsonData = XLSX.utils.sheet_to_json(firstSheet, { header: 1 });
      data = jsonData.map((row: any) =>
        row.map((cell: any) => cell?.toString() || '')
      );
    }

    setBomData(data);
  };

  const handleClear = () => {
    setSelectedFile(null);
    setBomData([]);
    setSellerResults([]);
  };

  const handleProcessBOM = async () => {
    if (!selectedFile) {
      toast({
        title: "No file selected",
        description: "Please select a BOM file first",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    try {
      const result = await apiClient.processBOM(selectedFile);
      setSellerResults(result.seller_info);
      toast({
        title: "Processing complete!",
        description: `Found seller information for ${result.seller_info.length} items`,
      });
    } catch (error) {
      console.error("Error processing BOM:", error);
      toast({
        title: "Processing failed",
        description: error instanceof Error ? error.message : "An unknown error occurred",
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <div className="container mx-auto px-4 py-12 max-w-6xl">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Package className="w-10 h-10 text-primary" />
            <h1 className="text-4xl font-bold text-gray-900">
              BOM Upload Portal
            </h1>
          </div>
          <p className="text-lg text-gray-600">
            Upload and preview your Bill of Materials files
          </p>
        </div>

        {/* Upload Section */}
        <div className="space-y-6">
          <FileUpload
            onFileSelect={handleFileSelect}
            selectedFile={selectedFile}
            onClear={handleClear}
          />

          {/* Preview Section */}
          {bomData.length > 0 && (
            <>
              <BOMPreview data={bomData} />

              {/* Process Button */}
              <div className="flex justify-center">
                <Button
                  onClick={handleProcessBOM}
                  disabled={isProcessing}
                  size="lg"
                  className="min-w-[200px]"
                >
                  {isProcessing ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    "Find Sellers"
                  )}
                </Button>
              </div>
            </>
          )}

          {/* Seller Results */}
          {sellerResults.length > 0 && <SellerResults results={sellerResults} />}
        </div>

        {/* Info Section */}
        {!selectedFile && (
          <div className="mt-12 grid md:grid-cols-3 gap-6">
            <div className="text-center p-6">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📄</span>
              </div>
              <h3 className="font-semibold mb-2">Multiple Formats</h3>
              <p className="text-sm text-gray-600">
                Support for CSV, Excel, and text files
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">👁️</span>
              </div>
              <h3 className="font-semibold mb-2">Instant Preview</h3>
              <p className="text-sm text-gray-600">
                See your BOM data immediately after upload
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🔒</span>
              </div>
              <h3 className="font-semibold mb-2">Client-Side Only</h3>
              <p className="text-sm text-gray-600">
                Your files stay in your browser, never uploaded to a server
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;