
"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { ToolCardProps } from "@/lib/types";
export function ToolCard({
  title,
  children,
}: ToolCardProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border rounded-xl bg-white shadow-sm my-3 overflow-hidden transition-all duration-300 hover:shadow-md">
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        className="w-full flex items-center justify-between px-4 py-3 bg-linear-to-r from-indigo-50 to-blue-50 hover:bg-indigo-100 transition-colors"
      >
        <h3 className="font-semibold text-sm">{title}</h3>
        <ChevronDown
          size={16}
          className={`transition-transform duration-300 ${isOpen ? "rotate-180" : ""}`}
        />
      </button>
      <div
        className={`transition-all duration-300 ease-in-out overflow-hidden ${
          isOpen ? "max-h-125 opacity-100" : "max-h-0 opacity-0"
        }`}
      >
        <div className="px-4 pb-4 text-sm text-gray-700">{children}</div>
      </div>
    </div>
  );
}
