<?php
namespace app;

class Fetch
{
    protected $curl;
    protected $headers = [];
    public function __construct()
    {
        $this->curl = curl_init();
        $this->set(CURLOPT_RETURNTRANSFER, true);
        $this->set(CURLOPT_HEADER, true);
    }

    public function set(int $opt, mixed $value)
    {
        curl_setopt($this->curl, $opt, $value);
        return $this;
    }

    public function get(string $url, array $data = [])
    {
        $this->set(CURLOPT_HTTPGET, true);
        $query = "?";
        foreach ($data as $k => $v) {
            $query .= $k . "=" . $v . "&";
        }
        rtrim($query, "&");
        $this->set(CURLOPT_URL, $url . $query);
        return $this;
    }

    public function post(string $url, array $data = [])
    {
        $this->set(CURLOPT_CUSTOMREQUEST, "POST");
        $this->set(CURLOPT_URL, $url);
        $this->set(CURLOPT_POSTFIELDS, json_encode($data));
        $this->header("Content-Type", "application/json");
        return $this;
    }

    public function header(string $k, string $v)
    {
        array_push($this->headers, $k . ":" . $v);
        return $this;
    }

    public function headers(array $_headers)
    {
        foreach ($_headers as $k => $v) {
            array_push($this->headers, $k . ":" . $v);
        }
        return $this;
    }

    public function send()
    {
        $this->set(CURLOPT_HTTPHEADER, $this->headers);
        return curl_exec($this->curl);
    }

    public function close()
    {
        curl_close($this->curl);
    }

}