import { Card } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { ScrollArea } from "@/components/ui/scroll-area";

interface BOMPreviewProps {
  data: string[][];
}

const BOMPreview = ({ data }: BOMPreviewProps) => {
  if (!data || data.length === 0) {
    return null;
  }

  const headers = data[0];
  const rows = data.slice(1);

  return (
    <Card className="p-6">
      <h3 className="text-lg font-semibold mb-4">Bill of Materials Preview</h3>
      <ScrollArea className="h-[400px] w-full rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              {headers.map((header, index) => (
                <TableHead key={index} className="font-semibold">
                  {header}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {rows.map((row, rowIndex) => (
              <TableRow key={rowIndex}>
                {row.map((cell, cellIndex) => (
                  <TableCell key={cellIndex}>{cell}</TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </ScrollArea>
      <p className="text-sm text-gray-500 mt-4">
        Showing {rows.length} items
      </p>
    </Card>
  );
};

export default BOMPreview;