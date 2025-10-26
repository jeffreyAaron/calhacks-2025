import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ExternalLink, Package } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Seller {
  company: string;
  link: string;
}

interface ItemWithSellers {
  name: string;
  quantity: number;
  sellers: Seller[];
}

interface SellerResultsProps {
  results: ItemWithSellers[];
}

const SellerResults = ({ results }: SellerResultsProps) => {
  if (!results || results.length === 0) {
    return null;
  }

  return (
    <div className="space-y-6 animate-in fade-in-50 duration-500">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Package className="w-5 h-5" />
            Seller Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {results.map((item, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-semibold text-lg">{item.name}</h3>
                    <p className="text-sm text-gray-600">Quantity: {item.quantity}</p>
                  </div>
                </div>

                {item.sellers && item.sellers.length > 0 ? (
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Seller</TableHead>
                        <TableHead>Link</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {item.sellers.map((seller, sellerIndex) => (
                        <TableRow key={sellerIndex}>
                          <TableCell className="font-medium">{seller.company}</TableCell>
                          <TableCell>
                            <Button
                              variant="link"
                              size="sm"
                              className="p-0 h-auto"
                              onClick={() => window.open(seller.link, '_blank')}
                            >
                              <ExternalLink className="w-4 h-4 mr-1" />
                              Visit Site
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                ) : (
                  <p className="text-sm text-gray-500 italic">No sellers found</p>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SellerResults;
