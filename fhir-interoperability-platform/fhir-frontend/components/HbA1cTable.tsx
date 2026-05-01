"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine
} from "recharts";

interface HbA1cData {
  date: string;
  value: string;
  type: string;
  source: string;
}

interface HbA1cTableProps {
  data: HbA1cData[];
}



export default function HbA1cTable({ data }: HbA1cTableProps) {
  
  const chartData = (data || [])
    .map((item) => ({
      ...item,
      numericValue: parseFloat(item.value.replace("%", ""))
    }))
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  const placeholderRows = Array(5).fill(null);
  return (
    <div className="bg-white rounded-xl shadow-sm border border-zinc-200 overflow-hidden">

      <div className="p-4 border-b border-zinc-100">
        <h3 className="text-sm font-bold text-[#4A5568] uppercase tracking-tight">
          Unified Longitudinal HbA1c Trend (Consolidated)
        </h3>
      </div>

      <div className="p-6 bg-zinc-50/30 border-b border-zinc-100">
        {chartData.length > 0 ? (
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 5, right: 10, bottom: 5, left: -20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
                <XAxis 
                  dataKey="date" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#94A3B8', fontSize: 10, fontWeight: 600 }}
                  dy={10}
                  tickFormatter={(value) => value.split(',')[0]}
                />
                <YAxis 
                  domain={['dataMin - 1', 'dataMax + 1']} 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#94A3B8', fontSize: 10, fontWeight: 600 }}
                />
                <Tooltip 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                {/* Clinical Goal Reference Line at 7% */}
                <ReferenceLine y={7} stroke="#10B981" strokeDasharray="3 3" label={{ value: 'GOAL', position: 'right', fill: '#10B981', fontSize: 10 }} />
                <Line 
                  type="monotone" 
                  dataKey="numericValue" 
                  stroke="#3B82F6" 
                  strokeWidth={3} 
                  dot={{ r: 4, fill: '#3B82F6', strokeWidth: 2, stroke: '#fff' }}
                  activeDot={{ r: 6 }}
                  name="HbA1c %"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="h-48 flex items-center justify-center text-zinc-400 italic text-sm">
            Insufficient data to plot trend graph.
          </div>
        )}
      </div>


      <div className="p-0">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="text-zinc-500 border-b border-zinc-100">
              <th className="px-4 py-3 font-semibold">Date</th>
              <th className="px-4 py-3 font-semibold">HbA1c Value (%)</th>
              <th className="px-4 py-3 font-semibold">Record Type</th>
              <th className="px-4 py-3 font-semibold">Data Source</th>
            </tr>
          </thead>




          
          <tbody className="divide-y divide-zinc-100">
            {data && data.length > 0 ? (
              data.map((row, i) => (
                <tr key={i} className="text-zinc-700 hover:bg-zinc-50 transition-colors">
                  <td className="px-4 py-3 font-medium">{row.date}</td>
                  <td className="px-4 py-3 font-bold text-[#2D3748]">{row.value}</td>
                  
                  {/* this is placeholder for  Record Type */}
                  <td className="px-4 py-3 text-zinc-400 italic">N/A</td>
                  
                  {/* placeholder for Source data */}
                  <td className="px-4 py-3 text-zinc-400 italic text-xs">Pending Lab Metadata</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-zinc-400">
                  No HbA1c observations found in patient's record.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}